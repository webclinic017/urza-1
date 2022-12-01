from trading.lemon_markets.credentials import market_data_key
import requests, json


class LemonMarketsWrapper:
    def __init__(self):
        pass

    def get_latest_quote(self, isin):
        request = requests.get(f"https://data.lemon.markets/v1/quotes/latest?isin={isin}",
                               headers={"Authorization": f"Bearer {market_data_key}"})
        return request.json()

    def get_timeseries(self, isin, step="d1"):
        request = requests.get(f"https://data.lemon.markets/v1/ohlc/{step}?isin={isin}&from=2021-11-01&limit=10",
                               headers={"Authorization": f"Bearer {market_data_key}"})
        return request.json()
