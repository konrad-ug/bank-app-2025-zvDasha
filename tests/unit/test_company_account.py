from src.company_account import CompanyAccount 

class TestCompanyAccount:
    def test_company_account_creation(self):
        account = CompanyAccount("TechCorp", "1234567890")
        assert account.company_name == "TechCorp"
        assert account.nip == "1234567890"
        assert account.balance == 0.0

# testy nip

    def test_company_account_invalid_nip(self):
        account = CompanyAccount("MegaFirm", "12345")
        assert account.nip == "Invalid"

        account = CompanyAccount("BigFirm", "abcdefghij")  
        assert account.nip == "Invalid"

        account = CompanyAccount("BigBoss", "12345678901")  
        assert account.nip == "Invalid"

# Nie ma promocji

    def test_company_account_no_promo_bonus(self):
        account = CompanyAccount("PromoFree", "1234567890")
        assert account.balance == 0.0

#test Przelewy
    def test_company_account_incoming_transfer(self):
        account = CompanyAccount("Tech", "1234567890")
        account.balance = 100.0
        account.incoming_transfer(50)
        assert account.balance == 150.0

    def test_company_account_outcoming_transfer(self):
        account = CompanyAccount("TechNew", "1234567890")
        account.balance = 100.0
        account.outcoming_transfer(50)
        assert account.balance == 50.0

    def test_company_account_incoming_transfer(self):
        account = CompanyAccount("Tech", "1234567890")
        account.balance = 100.0
        account.outcoming_transfer(150)
        assert account.balance == 100.0
