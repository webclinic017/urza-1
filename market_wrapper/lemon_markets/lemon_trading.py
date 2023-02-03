import json

import requests

from market_wrapper.lemon_markets.utils import create_idempotency, format_currency, get_base_url


class LemonTradingWrapper:

    @staticmethod
    def place_order(trading_key, paper, isin, side, quantity, expires_at, stop_price=None, limit_price=None,
                    notes=None):
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

        try:
            request = requests.post(get_base_url(paper),
                                    data=json.dumps(data),
                                    headers={"Authorization": f"Bearer {trading_key}"})
        except requests.exceptions.RequestException:
            return {"status": "error", "error_type": "connection"}
        return request.json()

    @staticmethod
    def activate_order(trading_key, paper, order_id, pin):
        try:
            request = requests.get(f"{get_base_url(paper)}orders/{order_id}/activate",
                                   data=json.dumps({"pin": pin}),
                                   headers={"Authorization": f"Bearer {trading_key}"})
        except requests.exceptions.RequestException:
            return {"status": "error", "error_type": "connection"}
        return request.json()

    @staticmethod
    def get_orders(trading_key, paper):
        try:
            request = requests.get(f"{get_base_url(paper)}orders/",
                                   headers={"Authorization": f"Bearer {trading_key}"})
        except requests.exceptions.RequestException:
            return {"status": "error", "error_type": "connection"}
        return request.json()

    @staticmethod
    def delete_order(trading_key, paper, order_id):
        try:
            request = requests.delete(f"{get_base_url(paper)}orders/{order_id}",
                                      headers={"Authorization": f"Bearer {trading_key}"})
        except requests.exceptions.RequestException:
            return {"status": "error", "error_type": "connection"}
        return request.json()

    @staticmethod
    def get_positions(trading_key, paper):
        try:
            request = requests.get(f"{get_base_url(paper)}positions",
                                   headers={"Authorization": f"Bearer {trading_key}"})
        except requests.exceptions.RequestException:
            return {"status": "error", "error_type": "connection"}
        return request.json()
