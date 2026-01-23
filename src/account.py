class Account:
    def __init__(self, balance=0.0):
        self.balance = balance
        self.history = [] 

    def incoming_transfer(self, amount):
        if amount > 0:
            self.balance += amount
            self.history.append(amount)

    def outcoming_transfer(self, amount):
        if amount > 0 and amount <= self.balance:
            self.balance -= amount
            self.history.append(-amount)

    def express_outgoing_transfer(self, amount):
        if amount <= 0:
            return
        fee = self.express_transfer_fee()

        if self.balance < amount:
            self.balance = -fee
            self.history.append(-amount)  
            self.history.append(-fee)    
            return

        self.balance -= (amount + fee)
        self.history.append(-amount)        
        self.history.append(-fee)         
    

    