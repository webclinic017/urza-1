from trading.lemon_markets.credentials import paper_trading_key, trading_key
from trading.lemon_markets.helpers import format_currency, create_idempotency
import requests, json


class LemonAccountWrapper:
    def __init__(self, paper):
        if paper:
            self.base_url = "https://paper-trading.lemon.markets/v1/account"
            self.key = paper_trading_key
        else:
            self.base_url = "https://trading.lemon.markets/v1/account"
            self.key = trading_key

    def get_account_info(self):
        request = requests.get(f"{self.base_url}",
                               headers={"Authorization": f"Bearer {self.key}"})
        return request.json()

    def withdraw(self, amount, pin):
        request = requests.post(f"{self.base_url}withdrawals",
                                data=json.dumps({"amount": format_currency(amount), "pin": pin,
                                                 "idempotency": create_idempotency()}),
                                headers={"Authorization": f"Bearer {self.key}"})
        return request.json()

    def get_withdrawals(self):
        request = requests.get(f"{self.base_url}withdrawals",
                               headers={"Authorization": f"Bearer {self.key}"})
        return request.json()

    def get_bank_statements(self):
        request = requests.get(f"{self.base_url}bankstatements",
                               headers={"Authorization": f"Bearer {self.key}"})
        return request.json()

    def get_documents(self):
        request = requests.get(f"{self.base_url}documents",
                               headers={"Authorization": f"Bearer {self.key}"})
        return request.json()

    def get_document(self, document_id):
        request = requests.get(f"{self.base_url}documents{document_id}",
                               headers={"Authorization": f"Bearer {self.key}"})
        return request.json()
