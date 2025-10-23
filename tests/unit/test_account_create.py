from src.account import Account


class TestAccount:
    def test_account_creation(self):
        account = Account("John", "Doe", "12345678910")
        assert account.first_name == "John"
        assert account.last_name == "Doe"
        assert account.balance == 0 
        assert account.pesel == "12345678910"


# testy PESEL
    def test_pesel_too_short(self):
        account = Account("Jane", "Doe","12345" )
        assert account.pesel == "Invalid"

    def test_pesel_too_long(self):
        account = Account("Jane", "Doe","1234512345678" )
        assert account.pesel == "Invalid" 
    
    def test_pesel_is_none(self):
        account = Account("Jane", "Doe", None )
        assert account.pesel == "Invalid" 



# testy PROMO_CODE 
    def test_correct_promo_code(self):
        account = Account("Jane", "Doe", "12345678910", "PROM_123")
        assert account.balance == 50
    
    def test_without_promo_code(self):
        account = Account("Joe", "Doe", "12345678901")
        assert account.balance == 0.0

    def test_wrong_len_promo_code(self):
        account = Account("Joe", "Doe", "12345678901","PROM_23")    
        assert account.balance == 0.0  

        account = Account("Joe", "Doe", "12345678901","PROM_1323")    
        assert account.balance == 0.0  

        account = Account("Joe", "Doe", "12345678901","pro_123")    
        assert account.balance == 0.0  

        account = Account("Joe", "Doe", "12345678901","PROM_1")    
        assert account.balance == 0.0  


    def test_wrong_format_promo_code(self):
        account = Account("Joe", "Doe", "12345678901","PRO_132")    
        assert account.balance == 0.0                    

        account = Account("Joe", "Doe", "12345678901","ROM_132")    
        assert account.balance == 0.0  

        account = Account("Joe", "Doe", "12345678901","Prom_132")    
        assert account.balance == 0.0

        account = Account("Joe", "Doe", "12345678901","prom_132")    
        assert account.balance == 0.0      
        
        account = Account("Joe", "Doe", "12345678901","AAAA_132")    
        assert account.balance == 0.0 

        account = Account("Joe", "Doe", "12345678901","AROM_132")    
        assert account.balance == 0.0 

        account = Account("Joe", "Doe", "12345678901","AAs_Aaaa")    
        assert account.balance == 0.0 

# testy funkcji wyliczania roku urodzenia

    def test_is_born_after_1960_true(self):
        acc = Account("Anna", "Nowak", "61010112345")
        assert acc.is_born_after_1960() is True

    def test_is_born_after_1960_false(self):
        acc = Account("Adam", "Kowalski", "34010112345")
        assert acc.is_born_after_1960() is False

    def test_is_born_with_wrong_pesel(self):
        acc = Account("Ewa", "Nowak", "123")
        assert acc.is_born_after_1960() is False

# testy dla PROMO_CODE kto urodził  się po 1960

    def test_after_1960_with_promo_code(self):
        acc = Account("Joe", "Doe", "61010112345", promotion_code="PROM_123")
        assert acc.balance == 50.0

    def test_before_1960_with_promo_code(self):
        acc = Account("Joe", "Doe", "44010112345", promotion_code="PROM_123")
        assert acc.balance == 0.0

    def test_after_1960_without_promo_code(self):
        acc = Account("Joe", "Doe", "61010112345")
        assert acc.balance == 0.0


    def test_wrong_pesel_with_promo_code(self):
        acc = Account("Joe", "Doe", "610112345", promotion_code="PROM_123")
        assert acc.balance == 0.0

    def test_correct_pesel_with_wrong_promo_code(self):
        acc = Account("Joe", "Doe", "610112345", promotion_code="PROM_13")
        assert acc.balance == 0.0

    
        




