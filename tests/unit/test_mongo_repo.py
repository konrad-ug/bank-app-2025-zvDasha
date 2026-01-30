import unittest
from unittest.mock import MagicMock, patch
from src.mongo_accounts_repository import MongoAccountsRepository
from src.accounts_repository import AccountsRepository
from src.personal_account import PersonalAccount
from src.company_account import CompanyAccount


class TestMongoAccountsRepository(unittest.TestCase):

    @patch('src.mongo_accounts_repository.MongoClient')
    def test_save_all_personal_accounts(self, mock_client_cls):
        mock_client = mock_client_cls.return_value
        mock_db = mock_client['bank_db']
        mock_collection = mock_db['accounts']
        
        repo = MongoAccountsRepository()
        
        acc1 = PersonalAccount("Jan", "Kowalski", "60010112345")
        acc2 = PersonalAccount("Anna", "Nowak", "60010112346")
        accounts = [acc1, acc2]

        repo.save_all(accounts)

        mock_collection.delete_many.assert_called_once_with({})
        self.assertEqual(mock_collection.update_one.call_count, 2)

    @patch('src.mongo_accounts_repository.MongoClient')
    def test_load_all_personal_accounts(self, mock_client_cls):
        mock_client = mock_client_cls.return_value
        mock_db = mock_client['bank_db']
        mock_collection = mock_db['accounts']
        
        mock_data = [
            {"first_name": "Jan", "last_name": "Kowalski", "pesel": "90010112345", "balance": 100.0, "history": [100.0], "account_type": "personal"},
            {"first_name": "Anna", "last_name": "Nowak", "pesel": "92010112345", "balance": 200.0, "history": [], "account_type": "personal"}
        ]
        mock_collection.find.return_value = mock_data
        
        repo = MongoAccountsRepository()
        loaded_accounts = repo.load_all()

        self.assertEqual(len(loaded_accounts), 2)
        self.assertEqual(loaded_accounts[0].first_name, "Jan")
        self.assertEqual(loaded_accounts[0].balance, 100.0)
        self.assertEqual(loaded_accounts[1].last_name, "Nowak")

    @patch('src.mongo_accounts_repository.MongoClient')
    def test_load_all_company_accounts(self, mock_client_cls):
        mock_client = mock_client_cls.return_value
        mock_db = mock_client['bank_db']
        mock_collection = mock_db['accounts']
        
        mock_data = [
            {"company_name": "TestCorp", "nip": "1234567890", "balance": 5000.0, "history": [2000.0], "account_type": "company"}
        ]
        mock_collection.find.return_value = mock_data
        
        repo = MongoAccountsRepository()
        loaded_accounts = repo.load_all()
        
        self.assertEqual(len(loaded_accounts), 1)
        self.assertIsInstance(loaded_accounts[0], CompanyAccount)
        self.assertEqual(loaded_accounts[0].company_name, "TestCorp")
        self.assertEqual(loaded_accounts[0].balance, 5000.0)

    @patch('src.mongo_accounts_repository.MongoClient')
    def test_save_all_company_accounts(self, mock_client_cls):
        mock_client = mock_client_cls.return_value
        mock_db = mock_client['bank_db']
        mock_collection = mock_db['accounts']
        
        repo = MongoAccountsRepository()
        
        with patch.object(CompanyAccount, 'verify_nip_gov', return_value=True):
            acc = CompanyAccount("TestCorp", "1234567890")
        
        repo.save_all([acc])

        mock_collection.delete_many.assert_called_once_with({})
        self.assertEqual(mock_collection.update_one.call_count, 1)
        call_args = mock_collection.update_one.call_args
        self.assertEqual(call_args[0][0], {"nip": "1234567890"}) 

    def test_abstract_repository_inheritance(self):
        repo = MongoAccountsRepository()
        self.assertIsInstance(repo, AccountsRepository)
        
    def test_repository_close_method(self):
        repo = MongoAccountsRepository()

        repo.close()
    
    def test_abstract_methods_raise_not_implemented(self):
        with self.assertRaises(NotImplementedError):
            AccountsRepository.save_all(None, None)
        
        with self.assertRaises(NotImplementedError):
            AccountsRepository.load_all(None)
