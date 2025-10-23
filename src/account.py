class Account:
    def __init__(self, first_name, last_name, pesel):
        self.first_name = first_name
        self.last_name = last_name
        self.balance = 0.0
        self.pesel = pesel if self.pesel_is_valid(pesel) else "Invalid"

    def pesel_is_valid(self, pesel):
        if pesel is not None and len(pesel) == 11:
            return True 
        ## variant
        ## variant2
        # if pesel is not None and len(pesel) == 11:
        #     self.pesel = pesel
        # else:
        #     self.pesel = "Invalid"


    