from trading.lemon_markets.credentials import paper_trading_key, trading_key
from trading.lemon_markets.helpers import create_idempotency, format_currency
import requests, json


class LemonPositionsWrapper:
    def __init__(self, paper):
        if paper:
            self.base_url = "https://paper-trading.lemon.markets/v1/positions"
            self.key = paper_trading_key
        else:
            self.base_url = "https://trading.lemon.markets/v1/positions"
            self.key = trading_key

    def get_positions(self):
        request = requests.get(self.base_url,
                               headers={"Authorization": f"Bearer {self.key}"})
        return request.json()
