from trading.lemon_markets.credentials import paper_trading_key, trading_key, pin
from trading.lemon_markets.helpers import format_currency, create_idempotency
import requests, json


class LemonTradingWrapper:
    def __init__(self, paper):
        if paper:
            self.base_url = "https://paper-trading.lemon.markets/v1/"
            self.key = paper_trading_key
        else:
            self.base_url = "https://trading.lemon.markets/v1/"
            self.key = trading_key

    def get_account_info(self):
        request = requests.get(f"{self.base_url}account",
                               headers={"Authorization": f"Bearer {self.key}"})
        return request.json()

    def withdraw(self, amount, pin):
        request = requests.post(f"{self.base_url}account/withdrawals",
                                data=json.dumps({"amount": format_currency(amount), "pin": pin,
                                                 "idempotency": create_idempotency()}),
                                headers={"Authorization": f"Bearer {self.key}"})
        return request.json()

    def get_withdrawals(self):
        request = requests.get(f"{self.base_url}account/withdrawals",
                               headers={"Authorization": f"Bearer {self.key}"})
        return request.json()

    def get_bank_statements(self):
        request = requests.get(f"{self.base_url}account/bankstatements",
                               headers={"Authorization": f"Bearer {self.key}"})
        return request.json()

    def get_documents(self):
        request = requests.get(f"{self.base_url}account/documents",
                               headers={"Authorization": f"Bearer {self.key}"})
        return request.json()
