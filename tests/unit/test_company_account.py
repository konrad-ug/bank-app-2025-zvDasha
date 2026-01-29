import pytest
from unittest.mock import patch
import requests
import os
from src.company_account import CompanyAccount

@patch('src.company_account.requests.get')
def test_create_company_valid_nip(mock_get):
    mock_get.return_value.status_code = 200
    mock_get.return_value.json.return_value = {
        "result": {
            "subject": {
                "name": "Super Firma",
                "nip": "1234567890",
                "statusVat": "Czynny"
            }
        }
    }

    account = CompanyAccount("TechCorp", "1234567890")
    
    assert account.company_name == "TechCorp"
    assert account.nip == "1234567890"
    mock_get.assert_called_once()

@patch('src.company_account.requests.get')
def test_create_company_not_active(mock_get):
    mock_get.return_value.status_code = 200
    mock_get.return_value.json.return_value = {
        "result": {
            "subject": {
                "statusVat": "Zwolniony"
            }
        }
    }
    with pytest.raises(ValueError, match="Company not registered!!"):
        CompanyAccount("TechCorp", "1234567890")

@patch('src.company_account.requests.get')
def test_create_company_api_error(mock_get):
    mock_get.return_value.status_code = 404
    with pytest.raises(ValueError, match="Company not registered!!"):
        CompanyAccount("TechCorp", "1234567890")

@patch('src.company_account.requests.get')
def test_invalid_nip_length(mock_get):
    account = CompanyAccount("Company", "12345")
    assert account.nip == "Invalid"
    mock_get.assert_not_called()

@pytest.fixture
def company_account():
    with patch('src.company_account.requests.get') as mock_get:
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = {
            "result": {"subject": {"statusVat": "Czynny"}}
        }
        return CompanyAccount("TechCorp", "1234567890")

def test_company_account_creation(company_account):
    assert company_account.company_name == "TechCorp"
    assert company_account.nip == "1234567890"
    assert company_account.balance == 0.0

def test_company_account_no_promo_bonus():
    with patch('src.company_account.requests.get') as mock_get:
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = {
            "result": {"subject": {"statusVat": "Czynny"}}
        }
        account = CompanyAccount("PromoFree", "1234567890")
        assert account.balance == 0.0

def test_company_account_incoming_transfer(company_account):
    company_account.balance = 100.0
    company_account.incoming_transfer(50)
    assert company_account.balance == 150.0

def test_company_account_outcoming_transfer(company_account):
    company_account.balance = 100.0
    company_account.outcoming_transfer(50)
    assert company_account.balance == 50.0

@patch('src.company_account.requests.get')
def test_verify_nip_gov_network_error(mock_get):
    mock_get.side_effect = requests.RequestException("Network error")
    with pytest.raises(ValueError, match="Company not registered!!"):
        CompanyAccount("Company", "1234567890")

@patch('src.company_account.requests.get')
def test_verify_nip_gov_with_trailing_slash(mock_get):
    mock_get.return_value.status_code = 200
    mock_get.return_value.json.return_value = {
        "result": {
            "subject": {
                "statusVat": "Czynny"
            }
        }
    }
    
    with patch.dict('os.environ', {'BANK_APP_MF_URL': 'https://wl-test.mf.gov.pl'}):
        account = CompanyAccount("Company", "1234567890")
        assert account.nip == "1234567890"
        called_url = mock_get.call_args[0][0]
        assert "api/search/nip" in called_url