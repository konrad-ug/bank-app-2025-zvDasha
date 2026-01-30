from pymongo import MongoClient
from src.accounts_repository import AccountsRepository
from src.personal_account import PersonalAccount
from src.company_account import CompanyAccount
from unittest.mock import patch


class MongoAccountsRepository(AccountsRepository):
    def __init__(self):
        self._client = MongoClient('mongodb://localhost:27017/')
        self._db = self._client['bank_db']
        self._collection = self._db['accounts']

    def save_all(self, accounts):
        self._collection.delete_many({})
        for account in accounts:
            account_data = account.to_dict()
            account_data['account_type'] = 'company' if isinstance(account, CompanyAccount) else 'personal'
            
            unique_key = {"nip": account.nip} if isinstance(account, CompanyAccount) else {"pesel": account.pesel}
            self._collection.update_one(unique_key, {"$set": account_data}, upsert=True)

    def load_all(self):
        accounts_data = self._collection.find({})
        accounts = []
        
        for data in accounts_data:
            if data.get('account_type') == 'company':
                with patch.object(CompanyAccount, 'verify_nip_gov', return_value=True):
                    acc = CompanyAccount(data["company_name"], data["nip"])
                    acc.balance = data["balance"]
                    acc.history = data["history"]
                    accounts.append(acc)
            else:
                acc = PersonalAccount(data["first_name"], data["last_name"], data["pesel"])
                acc.balance = data["balance"]
                acc.history = data["history"]
                accounts.append(acc)
        
        return accounts
