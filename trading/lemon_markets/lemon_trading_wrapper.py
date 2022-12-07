from trading.lemon_markets.credentials import paper_trading_key, trading_key
from trading.lemon_markets.helpers import create_idempotency, format_currency
import requests, json


class LemonTradingWrapper:
    def __init__(self, paper):
        if paper:
            self.base_url = "https://paper-trading.lemon.markets/v1/orders"
            self.key = paper_trading_key
        else:
            self.base_url = "https://trading.lemon.markets/v1/orders"
            self.key = trading_key

    def place_order(self, isin, side, quantity, expires_at, stop_price=None, limit_price=None, notes=None):
        data = {
            "isin": isin,
            "expires_at": expires_at,
            "side": side,
            "quantity": quantity,
            "venue": "XMUN",
            "idempotency": create_idempotency()
        }
        if stop_price is not None:
            data["stop_price"] = format_currency(stop_price)
        if limit_price is not None:
            data["stop_price"] = format_currency(stop_price)
        if notes is not None:
            data["notes"] = notes
        request = requests.post(self.base_url,
                                data=json.dumps(data),
                                headers={"Authorization": f"Bearer {self.key}"})
        return request.json()

    def activate_order(self, order_id, pin):
        request = requests.get(f"{self.base_url}/{order_id}/activate",
                               data=json.dumps({"pin": pin}),
                               headers={"Authorization": f"Bearer {self.key}"})
        return request.json()
