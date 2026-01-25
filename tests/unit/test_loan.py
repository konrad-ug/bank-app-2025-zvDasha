import pytest
from src.personal_account import PersonalAccount
from src.company_account import CompanyAccount


# testy o nadaniu kredytu dla PersonalAccount
@pytest.fixture
def personal_sut():
    return PersonalAccount("John", "Temsi", "12345678901")

@pytest.mark.parametrize("history, loan_amount, expected_result", [
    ([100, 100, 100], 500, True),
    ([50, 50, 50], 100, True),
    ([100, 100, 100, -50, 250], 400, True),
    ([100, 100, 100, -50, 250], 600, False),
    ([100, 100], 500, False),
    ([100, -100, 100], 500, False)
])
def test_personal_loan_logic(personal_sut, history, loan_amount, expected_result):
    personal_sut.history = history
    result = personal_sut.submit_for_loan(loan_amount)
    assert result == expected_result

def test_personal_loan_increases_balance(personal_sut):
    personal_sut.history = [100, 100, 100] 
    balance = personal_sut.balance
    personal_sut.submit_for_loan(500)
    assert personal_sut.balance == balance + 500
    
def test_loan_in_history(personal_sut):
    personal_sut.history = [100, 100, 100]
    personal_sut.submit_for_loan(500)
    assert personal_sut.history == [100, 100, 100, 500]

def test_rejected_loan_not_in_history(personal_sut):
    personal_sut.history = [100, -100]
    personal_sut.submit_for_loan(500)
    assert personal_sut.history == [100, -100]


# testy o nadaniu kredytu dla CompanyAccount
@pytest.fixture
def company_sut():
    return CompanyAccount("New Company", "1234567890")

@pytest.mark.parametrize("balance, history, loan_amount, expected_result", [
    (2000, [-1775], 1000, True),
    (5000, [-100, -1775, 500], 1000, True),
    (1999, [-1775], 1000, False),
    (2000, [-100, -200], 1000, False),
    (2000, [-1776], 1000, False),
    (0, [-1775], 1000, False)
])
def test_company_loan_logic(company_sut, balance, history, loan_amount, expected_result):
    company_sut.balance = balance
    company_sut.history = history
    result = company_sut.take_loan(loan_amount)
    assert result == expected_result

def test_company_loan_increases_balance(company_sut):
    company_sut.balance = 2000
    company_sut.history = [-1775]
    initial_balance = 2000
    loan_amount = 1000
    company_sut.take_loan(loan_amount)
    assert company_sut.balance == initial_balance + loan_amount