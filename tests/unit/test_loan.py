import pytest
from src.personal_account import PersonalAccount
from src.company_account import CompanyAccount


# testy o nadaniu kredytu dla PersonalAccount
@pytest.fixture
def personal_loan():
    return PersonalAccount("John", "Temsi", "12345678901")

@pytest.mark.parametrize("history, loan_amount, expected_result", [
    ([100, 100, 100], 500, True),
    ([50, 50, 50], 100, True),
    ([100, 100, 100, -50, 250], 400, True),
    ([100, 100, 100, -50, 250], 600, False),
    ([100, 100], 500, False),
    ([100, -100, 100], 500, False)
])
def test_personal_loan_logic(personal_loan, history, loan_amount, expected_result):
    personal_loan.history = history
    result = personal_loan.submit_for_loan(loan_amount)
    assert result == expected_result

def test_personal_loan_increases_balance(personal_loan):
    personal_loan.history = [100, 100, 100] 
    balance = personal_loan.balance
    personal_loan.submit_for_loan(500)
    assert personal_loan.balance == balance + 500
    
def test_loan_in_history(personal_loan):
    personal_loan.history = [100, 100, 100]
    personal_loan.submit_for_loan(500)
    assert personal_loan.history == [100, 100, 100, 500]

def test_rejected_loan_not_in_history(personal_loan):
    personal_loan.history = [100, -100]
    personal_loan.submit_for_loan(500)
    assert personal_loan.history == [100, -100]


# testy o nadaniu kredytu dla CompanyAccount
@pytest.fixture
def company_loan():
    return CompanyAccount("New Company", "1234567890")

@pytest.mark.parametrize("balance, history, loan_amount, expected_result", [
    (2000, [-1775], 1000, True),
    (5000, [-100, -1775, 500], 1000, True),
    (1999, [-1775], 1000, False),
    (2000, [-100, -200], 1000, False),
    (2000, [-1776], 1000, False),
    (0, [-1775], 1000, False)
])
def test_company_loan_logic(company_loan, balance, history, loan_amount, expected_result):
    company_loan.balance = balance
    company_loan.history = history
    result = company_loan.take_loan(loan_amount)
    assert result == expected_result

def test_company_loan_increases_balance(company_loan):
    company_loan.balance = 2000
    company_loan.history = [-1775]
    initial_balance = 2000
    loan_amount = 1000
    company_loan.take_loan(loan_amount)
    assert company_loan.balance == initial_balance + loan_amount


def test_company_loan_records_history(company_loan):
    company_loan.balance = 5000
    company_loan.history = [100, -1775]
    company_loan.take_loan(2000)
    assert company_loan.history == [100, -1775, 2000]


def test_company_loan_rejection_keeps_state(company_loan):
    company_loan.balance = 1000
    company_loan.history = [100, -100]
    result = company_loan.take_loan(400)
    assert result is False
    assert company_loan.balance == 1000
    assert company_loan.history == [100, -100]