from src.personal_account import PersonalAccount
from src.company_account import CompanyAccount

class TestTransfers:
    # def test_incoming_transfer(self):
    #     assert account.balance == 100.0

#ZADANIE 6 (incoming_outcoming)

    def test_incoming_transfer(self):
        account = PersonalAccount("Alice", "Johnson", "12345678901")
        account.balance = 100.0
        account.incoming_transfer(50)
        assert account.balance == 150.0

    def test_outcoming_transfer(self):
        account = PersonalAccount("Joe", "Johnson", "12345678901")
        account.balance = 100.0
        account.outcoming_transfer(50)
        assert account.balance == 50.0

    def test_outcoming_transfer_exceeding_balance(self):
        account = PersonalAccount("Alice", "Johnson", "12345678901")
        account.balance = 30.0
        account.outcoming_transfer(50)
        assert account.balance == 30.0

    def test_incoming_transfer_negative_amount(self):
        account = PersonalAccount("Alice", "Johnson", "12345678901")
        account.incoming_transfer(-50)
        assert account.balance == 0.0

    def test_express_personal_correct(self):
        account = PersonalAccount("April", "Ban", "12345678901")
        account.balance = 100
        account.express_outgoing_transfer(50)
        assert account.balance == 49  

    def test_express_ompany_correct(self):
        account = CompanyAccount("ABC", "1234567890")
        account.balance = 100
        account.express_outgoing_transfer(50)
        assert account.balance == 45   

    def test_express_personal_equivalent_amount(self):
        account = PersonalAccount("Ali", "Ben", "12345678901")
        account.balance = 100
        account.express_outgoing_transfer(100)
        assert account.balance == -1

    def test_express_company_equivalent_amount(self):
        account = CompanyAccount("RBO", "1234567890")
        account.balance = 150
        account.express_outgoing_transfer(150)
        assert account.balance == -5  

    def test_express_personal_too_much(self):
        account = PersonalAccount("Ali", "Ran", "12345678901")
        account.balance = 90
        account.express_outgoing_transfer(100)
        assert account.balance == -1 

    def test_express_company_too_much(self):
        account = CompanyAccount("COB", "1234567890")
        account.balance = 140
        account.express_outgoing_transfer(150)
        assert account.balance == -5  
    
