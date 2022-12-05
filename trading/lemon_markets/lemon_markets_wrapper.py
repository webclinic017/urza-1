from trading.lemon_markets.credentials import market_data_key
import requests, json


class LemonMarketsWrapper:
    def __init__(self):
        pass

    def get_quote(self, isin):
        request = requests.get(f"https://data.lemon.markets/v1/quotes/latest?isin={isin}",
                               headers={"Authorization": f"Bearer {market_data_key}"})
        return request.json()

    def get_daily_bar_data(self, isin, start_date, frequency="d1"):
        request = requests.get(f"https://data.lemon.markets/v1/ohlc/{frequency}?isin={isin}&from={start_date}&limit=10",
                               headers={"Authorization": f"Bearer {market_data_key}"})
        return request.json()
