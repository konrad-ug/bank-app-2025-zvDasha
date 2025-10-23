class Account:
    def __init__(self, first_name, last_name, pesel, promotion_code = None):
        self.first_name = first_name
        self.last_name = last_name
        self.balance = 0.0
        self.pesel = pesel if self.pesel_is_valid(pesel) else "Invalid"
        
        self.promotion_code = promotion_code
        if promotion_code and len(promotion_code)==8 and promotion_code.startswith("PROM_"):
            if self.is_born_after_1960():
                self.balance += 50



    def pesel_is_valid(self, pesel):
        if pesel is not None and len(pesel) == 11:
            return True 
        ## variant
        ## variant2
        # if pesel is not None and len(pesel) == 11:
        #     self.pesel = pesel
        # else:
        #     self.pesel = "Invalid"\

    def get_birth_year_from_pesel(self):
        if self.pesel == "Invalid":
            return None

        y = int(self.pesel[:2])
        m = int(self.pesel[2:4])
    
        if m > 12: 
            return 2000 + y
        else:
            return 1900 + y

    def is_born_after_1960(self):
            year = self.get_birth_year_from_pesel()
            if year is None:
                return False
            return year > 1960
    
    