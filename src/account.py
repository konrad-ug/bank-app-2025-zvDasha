from datetime import datetime
from smtp.smtp import SMTPClient

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

    def to_dict(self):
        return {
            "balance": self.balance,
            "history": self.history
        }
        self.history.append(-amount)        
        self.history.append(-fee)         
    

    def send_history_via_email(self, email_address: str) -> bool:
        today_date = datetime.today().strftime("%Y-%m-%d")
        subject = f"Account Transfer History {today_date}"
        text = f"{self._history_message_prefix()}: {self.history}"
        smtp = SMTPClient()
        return smtp.send(subject, text, email_address)

    def _history_message_prefix(self):
        return "Account history"

    