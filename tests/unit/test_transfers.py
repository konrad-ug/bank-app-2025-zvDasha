from src.account import Account

class TestTransfers:
    # def test_incoming_transfer(self):
    #     assert account.balance == 100.0

#ZADANIE 6 (incoming_outcoming)

    def test_incoming_transfer(self):
        account = Account("Alice", "Johnson", "12345678901")
        account.balance = 100.0
        account.incoming_transfer(50)
        assert account.balance == 150.0

    def test_outcoming_transfer(self):
        account = Account("Joe", "Johnson", "12345678901")
        account.balance = 100.0
        account.outcoming_transfer(50)
        assert account.balance == 50.0

    def test_outcoming_transfer_exceeding_balance(self):
        account = Account("Alice", "Johnson", "12345678901")
        account.balance = 30.0
        account.outcoming_transfer(50)
        assert account.balance == 30.0

    def test_incoming_transfer_negative_amount(self):
        account = Account("Alice", "Johnson", "12345678901")
        account.incoming_transfer(-50)
        assert account.balance == 0.0