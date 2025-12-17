class Account:
    def __init__(self, balance=0.0):
        self.balance = balance

    def incoming_transfer(self, amount):
        if amount > 0:
            self.balance += amount

    def outcoming_transfer(self, amount):
        if amount > 0 and amount <= self.balance:
            self.balance -= amount


    def express_outgoing_transfer(self, amount):
        if amount <= 0:
            return
        fee = self.express_transfer_fee()

        if self.balance < amount:
            self.balance = -fee
            return

        self.balance -= (amount + fee)
    

    