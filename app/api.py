from flask import Flask, request, jsonify
from src.personal_account import PersonalAccount
from src.account_registry import AccountsRegistry
from src.mongo_accounts_repository import MongoAccountsRepository

app = Flask(__name__)
registry = AccountsRegistry()
account_repository = MongoAccountsRepository()

@app.route("/api/accounts", methods=['POST'])
def create_account():
    data = request.get_json()
    print(f"Received account creation request: {data}")

    if "name" not in data or "surname" not in data or "pesel" not in data:
        return jsonify({"message": "Missing required fields"}), 400

    if registry.get_account_by_pesel(data["pesel"]):
        return jsonify({"message": "An account with this PESEL number already exists."}), 409

    account = PersonalAccount(data["name"], data["surname"], data["pesel"])
    registry.add_account(account)
    return jsonify({"message": "Account created"}), 201

@app.route("/api/accounts", methods=['GET'])
def get_all_accounts():
    accounts = registry.get_all_accounts()
    accounts_data = [
        {
            "name": acc.first_name, 
            "surname": acc.last_name, 
            "pesel": acc.pesel, 
            "balance": acc.balance
        } 
        for acc in accounts
    ]
    return jsonify(accounts_data), 200

@app.route("/api/accounts/count", methods=['GET'])
def get_account_count():
    count = registry.number_of_accounts()
    return jsonify({"count": count}), 200


@app.route("/api/accounts/<pesel>", methods=['GET'])
def get_account_by_pesel(pesel):
    account = registry.get_account_by_pesel(pesel)
    if account:
        return jsonify({
            "name": account.first_name, 
            "surname": account.last_name, 
            "pesel": account.pesel, 
            "balance": account.balance
        }), 200
    else:
        return jsonify({"message": "Account not found"}), 404
    
@app.route("/api/accounts/<pesel>", methods=['PATCH'])
def update_account(pesel):
    account = registry.get_account_by_pesel(pesel)
    if account is None:
        return jsonify({"message": "Account not found"}), 404
    
    data = request.get_json()
    if "name" in data:
        account.first_name = data["name"]
    if "surname" in data:
        account.last_name = data["surname"]
    
    return jsonify({"message": "Account updated"}), 200

@app.route("/api/accounts/<pesel>", methods=['DELETE'])
def delete_account(pesel):
    account = registry.get_account_by_pesel(pesel)
    if account is None:
        return jsonify({"message": "Account not found"}), 404
    registry.accounts.remove(account)
    return jsonify({"message": "Account deleted"}), 200

@app.route("/api/accounts/<pesel>/transfer", methods=['POST'])
def transfer(pesel):
    account = registry.get_account_by_pesel(pesel)
    if not account:
        return jsonify({"message": "Account not found"}), 404
    
    data = request.get_json()
    if "amount" not in data or "type" not in data:
        return jsonify({"message": "Missing amount or type"}), 400

    amount = float(data["amount"])
    transfer_type = data["type"]

    if transfer_type == "incoming":
        account.incoming_transfer(amount)
        return jsonify({"message": "Order accepted for processing"}), 200

    elif transfer_type == "outgoing":
        if account.balance < amount:
            return jsonify({"message": "Not enough money"}), 422
        account.outcoming_transfer(amount)
        return jsonify({"message": "Order accepted for processing"}), 200

    elif transfer_type == "express":
        fee = account.express_transfer_fee()
        if account.balance < (amount + fee):
             return jsonify({"message": "Not enough money"}), 422
        account.express_outgoing_transfer(amount)
        return jsonify({"message": "Order accepted for processing"}), 200
    else:
        return jsonify({"message": "Invalid transfer type"}), 400

@app.route("/api/accounts/save", methods=['POST'])
def save_accounts():
    account_repository.save_all(registry.get_all_accounts())
    return jsonify({"message": "Accounts saved successfully"}), 200

@app.route("/api/accounts/load", methods=['POST'])
def load_accounts():
    registry.accounts = account_repository.load_all()
    return jsonify({"message": "Accounts loaded successfully"}), 200

if __name__ == "__main__":
    app.run(debug=True)