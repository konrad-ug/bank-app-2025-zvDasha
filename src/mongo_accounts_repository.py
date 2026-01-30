from pymongo import MongoClient
from src.personal_account import PersonalAccount

class MongoAccountsRepository:
    def __init__(self):
        self._client = MongoClient('mongodb://localhost:27017/')
        self._db = self._client['bank_db']
        self._collection = self._db['accounts']

    def save_all(self, accounts):
        self._collection.delete_many({})
        for account in accounts:
            self._collection.update_one(
                {"pesel": account.pesel},
                {"$set": account.to_dict()},
                upsert=True,
            )

    def load_all(self):
        accounts_data = self._collection.find({})
        accounts = []
        for data in accounts_data:
            acc = PersonalAccount(data["first_name"], data["last_name"], data["pesel"])
            acc.balance = data["balance"]
            acc.history = data["history"]
            accounts.append(acc)
        return accounts
