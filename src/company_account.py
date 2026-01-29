from src.account import Account
import os
import requests
from datetime import datetime

class CompanyAccount(Account):
    def __init__(self, company_name, nip):
        super().__init__(balance=0.0)
        self.company_name = company_name
        
        if self.is_nip_valid(nip):
            if self.verify_nip_gov(nip):
                self.nip = nip
            else:
                raise ValueError("Company not registered!!")
        else:
            self.nip = "Invalid"

    def is_nip_valid(self, nip):
        if isinstance(nip, str) and len(nip)==10 and nip.isdigit():
            return True
        return False

    def verify_nip_gov(self, nip):
        base_url = os.getenv("BANK_APP_MF_URL", "https://wl-test.mf.gov.pl/")
        today = datetime.now().strftime("%Y-%m-%d")

        if not base_url.endswith("/"):
            base_url += "/"
            
        endpoint = f"{base_url}api/search/nip/{nip}?date={today}"
        
        try:
            print(f"Sending request to: {endpoint}")
            response = requests.get(endpoint)
            print(f"Response: {response.status_code}, {response.text}")
            
            if response.status_code == 200:
                data = response.json()
                if "result" in data and "subject" in data["result"]:
                    subject = data["result"]["subject"]
                    if subject and subject.get("statusVat") == "Czynny":
                        return True
            return False
            
        except requests.RequestException as e:
            print(f"Error connecting to MF API: {e}")
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
    
    def _history_message_prefix(self):
        return "Company account history"