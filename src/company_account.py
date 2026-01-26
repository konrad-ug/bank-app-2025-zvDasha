from src.account import Account

class CompanyAccount(Account):
    def __init__(self, company_name, nip):
        super().__init__(balance=0.0)
        self.company_name = company_name
        self.nip = nip if self.is_nip_valid(nip) else "Invalid"

    def is_nip_valid(self, nip):
        if isinstance(nip, str) and len(nip)==10 and nip.isdigit():
            return True
        return False

    def express_transfer_fee(self):
        return 5.0

    def take_loan(self, amount):
        if self.balance < 2 * amount:
            return False
        if -1775 not in self.history:
            return False
        self.balance += amount
        self.history.append(amount) 
        return True