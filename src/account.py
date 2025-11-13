from src.personal_account import PersonalAccount
from src.company_account import CompanyAccount

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
        if isinstance(self, PersonalAccount):
            fee = 1.0
        elif isinstance(self, CompanyAccount):
            fee = 5.0
        else:
            raise ValueError("Nieznany typ konta")

        if amount > 0 and (amount + fee) <= self.balance:
        self.balance -= (amount + fee)

    
    