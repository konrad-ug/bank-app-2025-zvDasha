import pytest
from src.account_registry import AccountsRegistry
from src.personal_account import PersonalAccount

@pytest.fixture
def account_registry():
    return AccountsRegistry()

def test_registry_initially_empty(account_registry):
    assert account_registry.number_of_accounts() == 0

def test_add_account(account_registry):
    account = PersonalAccount("Jan", "Kowalski", "12345678901")
    account_registry.add_account(account)
    assert account_registry.number_of_accounts() == 1

def test_get_all_accounts(account_registry):
    account1 = PersonalAccount("Jan", "Kowalski", "12345678901")
    account2 = PersonalAccount("Mia", "Kowalska", "12345678902")
    account_registry.add_account(account1)
    account_registry.add_account(account2)
    all_accounts = account_registry.get_all_accounts()
    assert len(all_accounts) == 2
    assert account1 in all_accounts and account2 in all_accounts

def test_get_account_by_pesel(account_registry):
    account = PersonalAccount("Jan", "Kowalski", "12345678901")
    account_registry.add_account(account)
    found_account = account_registry.get_account_by_pesel("12345678901")
    assert found_account == account

def test_get_account_by_pesel_not_found(account_registry):
    found_account = account_registry.get_account_by_pesel("00000000000")
    assert found_account is None