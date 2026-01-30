import unittest
from unittest.mock import MagicMock, patch
from app.api import app
from src.personal_account import PersonalAccount

class TestAccountSaveLoad(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    @patch('app.api.account_repository')
    @patch('app.api.registry')
    def test_save_accounts(self, mock_registry, mock_repo):
        acc1 = PersonalAccount("Jan", "Kowalski", "12345678901")
        mock_registry.get_all_accounts.return_value = [acc1]
  
        response = self.app.post('/api/accounts/save')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, {"message": "Accounts saved successfully"})
        mock_repo.save_all.assert_called_once_with([acc1])

    @patch('app.api.account_repository')
    @patch('app.api.registry')
    def test_load_accounts_clears_registry(self, mock_registry, mock_repo):
        acc1 = PersonalAccount("Jan", "Kowalski", "12345678901")
        mock_repo.load_all.return_value = [acc1]
        
        mock_accounts_list = MagicMock()
        mock_registry.accounts = mock_accounts_list

        response = self.app.post('/api/accounts/load')
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, {"message": "Accounts loaded successfully"})
        mock_accounts_list.clear.assert_called_once()
        mock_repo.load_all.assert_called_once()

    @patch('app.api.account_repository')
    @patch('app.api.registry')
    def test_load_accounts(self, mock_registry, mock_repo):
        acc1 = PersonalAccount("Jan", "Kowalski", "12345678901")
        loaded_accounts = [acc1]
        mock_repo.load_all.return_value = loaded_accounts
        mock_registry.accounts = []

        response = self.app.post('/api/accounts/load')
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, {"message": "Accounts loaded successfully"})
        mock_repo.load_all.assert_called_once()
