from src.account import Account

class PersonalAccount(Account):
    def __init__(self, first_name, last_name, pesel, promotion_code=None):
        super().__init__(balance=0.0)
        self.first_name = first_name
        self.last_name = last_name
        self.pesel = pesel if self.pesel_is_valid(pesel) else "Invalid"

        self.promotion_code = promotion_code
        if promotion_code and len(promotion_code) == 8 and promotion_code.startswith("PROM_"):
            if self.is_born_after_1960():
                self.balance += 50

    def pesel_is_valid(self, pesel):
        if pesel is not None and len(pesel) == 11:
            return True 

    def get_birth_year_from_pesel(self):
        if self.pesel == "Invalid":
            return None

        y = int(self.pesel[:2])
        m = int(self.pesel[2:4])
        if m > 12:
            return 2000 + y
        return 1900 + y

    def is_born_after_1960(self):
        year = self.get_birth_year_from_pesel()
        if year is None:
            return False
        return year > 1960

    def to_dict(self):
        data = super().to_dict()
        data.update({
            "first_name": self.first_name,
            "last_name": self.last_name,
            "pesel": self.pesel
        })
        return data

    def express_transfer_fee(self):
        return 1.0
    
    def submit_for_loan(self, amount):
    
        if len(self.history) >= 3 and all(t > 0 for t in self.history[-3:]):
            self.balance += amount
            self.history.append(amount)
            return True
        
        if len(self.history) >= 5 and sum(self.history[-5:]) > amount:
            self.balance += amount
            self.history.append(amount)
            return True
            
        return False
    
    def _history_message_prefix(self):
        return "Personal account history"