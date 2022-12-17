import json

import requests

from trading.lemon_markets.credentials import market_data_key
from trading.lemon_markets.helpers import concat_ISINs


class LemonMarketWrapper:
    def __init__(self):
        self.base_url = "https://data.lemon.markets/v1/"

    def get_quote_by_isin(self, ISINs, price="ask"):
        ISINs = concat_ISINs(ISINs)
        request = requests.get(f"{self.base_url}quotes/latest?isin={ISINs}",
                               headers={"Authorization": f"Bearer {market_data_key}"})
        results = request.json()["results"]

        return {result["isin"]: {"t": result["t"], "a_p": result["a"], "a_s": result["a_v"],
                                 "b_p": result["b"], "b_s": result["b_v"]} for result in results}

    def get_ohlc_data_by_isin(self, ISINs, start_date, frequency):
        if frequency.startswith("da"):
            frequency = "d1"
        elif frequency.startswith("hour"):
            frequency = "h1"
        elif frequency.startswith("minute"):
            frequency = "m1"
        else:
            ValueError("Invalid frequency specified.")

        request = requests.get(
            f"{self.base_url}ohlc/{frequency}?isin={concat_ISINs(ISINs)}&from={start_date.isoformat()}",
            headers={"Authorization": f"Bearer {market_data_key}"})
        results = request.json()["results"]

        if isinstance(ISINs, str):
            response = {ISINs: []}
        else:
            response = {isin: [] for isin in ISINs}
        for dp in results:
            response[dp["isin"]].append(
                {"t": dp["t"], "o": dp["o"], "h": dp["h"], "l": dp["l"], "c": dp["c"], "v": dp["v"], "pbv": dp["pbv"]})
        return response

    def get_instruments(self, search):
        """Search for Name, ISIN, WKN or symbol"""
        request = requests.get(f"{self.base_url}instruments",
                               data=json.dumps({"search": search}),
                               headers={"Authorization": f"Bearer {market_data_key}"})
        return request.json()
