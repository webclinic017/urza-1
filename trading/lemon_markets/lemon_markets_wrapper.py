from trading.lemon_markets.credentials import market_data_key
import requests, json


class LemonMarketsWrapper:
    def __init__(self):
        self.base_url = "https://data.lemon.markets/v1/"

    def get_quote(self, ISINs):
        ISINs = ",".join(isin for isin in ISINs)[1:]

        request = requests.get(f"{self.base_url}quotes/latest?isin={ISINs}",
                               headers={"Authorization": f"Bearer {market_data_key}"})
        return request.json()

    def get_ohlc_data(self, ISINs, start_date, frequency):
        if frequency.startswith("da"):
            frequency = "d1"
        elif frequency.startswith("hour"):
            frequency = "h1"
        elif frequency.startswith("minute"):
            frequency = "m1"
        else:
            ValueError("Invalid frequency specified.")

        ISINs = ",".join(isin for isin in ISINs)[1:]

        request = requests.get(f"{self.base_url}ohlc/{frequency}?isin={ISINs}&from={start_date.isoformat()}",
                               headers={"Authorization": f"Bearer {market_data_key}"})
        return request.json()

    def get_instruments(self, search):
        """Search for Name, ISIN, WKN or symbol"""
        request = requests.get(f"{self.base_url}instruments",
                               data=json.dumps({"search": search}),
                               headers={"Authorization": f"Bearer {market_data_key}"})
        return request.json()
