import pytest
from src.personal_account import PersonalAccount

@pytest.fixture
def sut():
    return PersonalAccount("John", "Temsi", "12345678901")

@pytest.mark.parametrize("history, loan_amount, expected_result", [
    ([100, 100, 100], 500, True),
    ([50, 50, 50], 100, True),
    ([100, 100, 100, -50, 250], 400, True),
    ([100, 100, 100, -50, 250], 600, False),
    ([100, 100], 500, False),
    ([100, -100, 100], 500, False)
])
def test_loan_logic(sut, history, loan_amount, expected_result):
    sut.history = history
    result = sut.submit_for_loan(loan_amount)
    assert result == expected_result

def test_loan_increases_balance(sut):
    sut.history = [100, 100, 100] 
    balance = sut.balance
    sut.submit_for_loan(500)
    assert sut.balance == balance + 500

def test_loan_in_history(sut):
    sut.history = [100, 100, 100]
    sut.submit_for_loan(500)
    assert sut.history == [100, 100, 100, 500]

def test_rejected_loan_not_in_history(sut):
    sut.history = [100, -100]
    sut.submit_for_loan(500)
    assert sut.history == [100, -100]