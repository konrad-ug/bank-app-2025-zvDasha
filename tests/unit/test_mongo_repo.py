import unittest
from unittest.mock import MagicMock, patch
from src.mongo_accounts_repository import MongoAccountsRepository
from src.personal_account import PersonalAccount

class TestMongoAccountsRepository(unittest.TestCase):

    @patch('src.mongo_accounts_repository.MongoClient')
    def test_save_all(self, mock_client_cls):
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
    def test_load_all(self, mock_client_cls):

        mock_client = mock_client_cls.return_value
        mock_db = mock_client['bank_db']
        mock_collection = mock_db['accounts']
        
        mock_data = [
            {"first_name": "Jan", "last_name": "Kowalski", "pesel": "90010112345", "balance": 100.0, "history": [100.0]},
            {"first_name": "Anna", "last_name": "Nowak", "pesel": "92010112345", "balance": 200.0, "history": []}
        ]
        mock_collection.find.return_value = mock_data
        
        repo = MongoAccountsRepository()

        loaded_accounts = repo.load_all()

        self.assertEqual(len(loaded_accounts), 2)
        self.assertEqual(loaded_accounts[0].first_name, "Jan")
        self.assertEqual(loaded_accounts[0].balance, 100.0)
        self.assertEqual(loaded_accounts[1].last_name, "Nowak")
