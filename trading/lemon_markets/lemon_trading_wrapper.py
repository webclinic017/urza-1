from trading.lemon_markets.credentials import paper_trading_key
import requests


class LemonTradingWrapper:
    def __init__(self, paper):
        if paper:
            self.base_url = "https://paper-trading.lemon.markets/v1/"
        else:
            self.base_url = "https://trading.lemon.markets/v1/"

    def get_account_info(self):
        request = requests.get("https://paper-trading.lemon.markets/v1/account",
                               headers={"Authorization": f"Bearer {paper_trading_key}"})
        return request.json()
