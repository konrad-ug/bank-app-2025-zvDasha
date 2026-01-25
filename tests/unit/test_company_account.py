from src.company_account import CompanyAccount 
import pytest

@pytest.fixture
def sut():
    return CompanyAccount("TechCorp", "1234567890")

def test_company_account_creation(sut):
    assert sut.company_name == "TechCorp"
    assert sut.nip == "1234567890"
    assert sut.balance == 0.0

@pytest.mark.parametrize("invalid_nip", [
    "12345",         
    "abcdefghij",    
    "12345678901",  
])
def test_company_account_invalid_nip(invalid_nip):
    account = CompanyAccount("Company", invalid_nip)
    assert account.nip == "Invalid"

def test_company_account_no_promo_bonus():
    account = CompanyAccount("PromoFree", "1234567890")
    assert account.balance == 0.0

def test_company_account_incoming_transfer(sut):
    sut.balance = 100.0
    sut.incoming_transfer(50)
    assert sut.balance == 150.0

def test_company_account_outcoming_transfer(sut):
    sut.balance = 100.0
    sut.outcoming_transfer(50)
    assert sut.balance == 50.0






# # -------- Testy do parametrizacji----------------------

# class TestCompanyAccount:
#     def test_company_account_creation(self):
#         account = CompanyAccount("TechCorp", "1234567890")
#         assert account.company_name == "TechCorp"
#         assert account.nip == "1234567890"
#         assert account.balance == 0.0

# # testy nip

#     def test_company_account_invalid_nip(self):
#         account = CompanyAccount("MegaFirm", "12345")
#         assert account.nip == "Invalid"

#         account = CompanyAccount("BigFirm", "abcdefghij")  
#         assert account.nip == "Invalid"

#         account = CompanyAccount("BigBoss", "12345678901")  
#         assert account.nip == "Invalid"

# # Nie ma promocji

#     def test_company_account_no_promo_bonus(self):
#         account = CompanyAccount("PromoFree", "1234567890")
#         assert account.balance == 0.0

# #test Przelewy
#     def test_company_account_incoming_transfer(self):
#         account = CompanyAccount("Tech", "1234567890")
#         account.balance = 100.0
#         account.incoming_transfer(50)
#         assert account.balance == 150.0

#     def test_company_account_outcoming_transfer(self):
#         account = CompanyAccount("TechNew", "1234567890")
#         account.balance = 100.0
#         account.outcoming_transfer(50)
#         assert account.balance == 50.0

#     def test_company_account_incoming_transfer(self):
#         account = CompanyAccount("Tech", "1234567890")
#         account.balance = 100.0
#         account.outcoming_transfer(150)
#         assert account.balance == 100.0
