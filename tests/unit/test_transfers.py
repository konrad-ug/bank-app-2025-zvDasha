from src.personal_account import PersonalAccount
from src.company_account import CompanyAccount
import pytest

class TestTransfers:
    # def test_incoming_transfer(self):
    #     assert account.balance == 100.0

# testy incoming/outcoming

    @pytest.fixture(autouse=True)
    def mock_gov_api(self, mocker):
        mock = mocker.patch("src.company_account.requests.get")
        mock.return_value.status_code = 200
        mock.return_value.json.return_value = {
            "result": {"subject": {"statusVat": "Czynny"}}
        }

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

    def test_express_transfer_zero_amount(self):
        account = PersonalAccount("John", "Doe", "12345678901")
        account.balance = 100
        account.express_outgoing_transfer(0)
        assert account.balance == 100 

    def test_express_transfer_negative_amount(self):
        account = PersonalAccount("Jane", "Doe", "12345678901")
        account.balance = 100
        account.express_outgoing_transfer(-50)
        assert account.balance == 100 


# testy Historia operacji

    def test_history_incoming_transfer(self):
        account = PersonalAccount("Alice", "Johnson", "12345678901")
        account.incoming_transfer(500)
        assert account.history == [500.0]

    def test_history_outcoming_transfer(self):
        account = PersonalAccount("Bob", "Smith", "12345678901")
        account.balance = 100
        account.outcoming_transfer(30)
        assert account.history == [-30.0]

    def test_history_multiple_operations(self):
        account = PersonalAccount("Charlie", "Brown", "12345678901")
        account.incoming_transfer(500)
        account.balance = 500
        account.outcoming_transfer(200)
        assert account.history == [500.0, -200.0]

    def test_history_express_transfer_personal(self):
        account = PersonalAccount("David", "Lee", "12345678901")
        account.balance = 100
        account.express_outgoing_transfer(50)
        assert account.history == [-50.0, -1.0]

    def test_history_express_transfer_company(self):
        account = CompanyAccount("TechCorp", "1234567890")
        account.balance = 100
        account.express_outgoing_transfer(50)
        assert account.history == [-50.0, -5.0]

    def test_history_complex_scenario(self):
        account = PersonalAccount("Eve", "White", "12345678901")
        account.incoming_transfer(500)
        account.balance = 500
        account.outcoming_transfer(100)
        account.express_outgoing_transfer(200)
        assert account.history == [500.0, -100.0, -200.0, -1.0]

    def test_history_insufficient_balance_express(self):
        account = PersonalAccount("Frank", "Black", "12345678901")
        account.balance = 20
        account.express_outgoing_transfer(100)
        assert account.history == [-100.0, -1.0] 

    def test_history_insufficient_balance_regular(self):
        account = PersonalAccount("Grace", "Green", "12345678901")
        account.balance = 20
        account.outcoming_transfer(100)
        assert account.history == []

    def test_history_negative_incoming_ignored(self):
        account = PersonalAccount("Henry", "Blue", "12345678901")
        account.incoming_transfer(-50)
        assert account.history == []
    
