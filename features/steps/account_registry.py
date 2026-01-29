from behave import *
import requests

URL = "http://127.0.0.1:5000"

@step('I create an account using name: "{name}", last name: "{last_name}", pesel: "{pesel}"')
def create_account(context, name, last_name, pesel):
    json_body = { 
        "name": f"{name}",
        "surname": f"{last_name}",
        "pesel": pesel
    }
    create_resp = requests.post(URL + "/api/accounts", json = json_body)
    assert create_resp.status_code == 201

@step('Account registry is empty')
def clear_account_registry(context):
    response = requests.get(URL + "/api/accounts")
    accounts = response.json()
    for account in accounts:
        pesel = account["pesel"]
        requests.delete(URL + f"/api/accounts/{pesel}")

@step('Number of accounts in registry equals: "{count}"')
def is_account_count_equal_to(context, count):
    response = requests.get(URL + "/api/accounts/count")
    assert response.status_code == 200
    assert response.json()["count"] == int(count)

@step('Account with pesel "{pesel}" exists in registry')
def check_account_with_pesel_exists(context, pesel):
    response = requests.get(URL + f"/api/accounts/{pesel}")
    assert response.status_code == 200

@step('Account with pesel "{pesel}" does not exist in registry')
def check_account_with_pesel_does_not_exist(context, pesel):
    response = requests.get(URL + f"/api/accounts/{pesel}")
    assert response.status_code == 404

@when('I delete account with pesel: "{pesel}"')
def delete_account(context, pesel):
    response = requests.delete(URL + f"/api/accounts/{pesel}")
    assert response.status_code == 200

@when('I update "{field}" of account with pesel: "{pesel}" to "{value}"')
def update_field(context, field, pesel, value):
    if field not in ["name", "surname"]:
        raise ValueError(f"Invalid field: {field}. Must be 'name' or 'surname'.")
    json_body = { f"{field}": f"{value}" }
    response = requests.patch(URL + f"/api/accounts/{pesel}", json = json_body)
    assert response.status_code == 200

@then('Account with pesel "{pesel}" has "{field}" equal to "{value}"')
def field_equals_to(context, pesel, field, value):
    response = requests.get(URL + f"/api/accounts/{pesel}")
    assert response.status_code == 200
    json_data = response.json()
    assert json_data[field] == value

# Transfer

@step('Account with pesel "{pesel}" has balance equal to "{balance}"')
def check_balance(context, pesel, balance):
    response = requests.get(URL + f"/api/accounts/{pesel}")
    assert response.status_code == 200
    actual_balance = response.json()["balance"]
    assert float(actual_balance) == float(balance)

@step('I make an incoming transfer of "{amount}" to account with pesel "{pesel}"')
def incoming_transfer(context, amount, pesel):
    json_body = {"amount": float(amount), "type": "incoming"}
    response = requests.post(URL + f"/api/accounts/{pesel}/transfer", json=json_body)
    assert response.status_code == 200

@when('I make an outgoing transfer of "{amount}" from account with pesel "{pesel}"')
def outgoing_transfer(context, amount, pesel):
    json_body = {"amount": float(amount), "type": "outgoing"}
    response = requests.post(URL + f"/api/accounts/{pesel}/transfer", json=json_body)
    assert response.status_code == 200

@when('I try to make an outgoing transfer of "{amount}" from account with pesel "{pesel}"')
def try_outgoing_transfer(context, amount, pesel):
    json_body = {"amount": float(amount), "type": "outgoing"}
    context.response = requests.post(URL + f"/api/accounts/{pesel}/transfer", json=json_body)

@step('The transfer should fail with status code "{status_code}"')
def check_transfer_fail(context, status_code):
    assert context.response.status_code == int(status_code)

@when('I make an express transfer of "{amount}" from account with pesel "{pesel}"')
def express_transfer(context, amount, pesel):
    json_body = {"amount": float(amount), "type": "express"}
    response = requests.post(URL + f"/api/accounts/{pesel}/transfer", json=json_body)
    assert response.status_code == 200