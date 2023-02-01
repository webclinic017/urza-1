import json

import requests

from trading.lemon_markets.credentials import market_data_key
from market.lemon_markets.utils import concat_ISINs


class LemonMarketWrapper:

    @staticmethod
    def get_quote_by_isin(ISINs):
        ISINs = concat_ISINs(ISINs)
        request = requests.get(f"https://data.lemon.markets/v1/quotes/latest?isin={ISINs}",
                               headers={"Authorization": f"Bearer {market_data_key}"})
        results = request.json()["results"]

        return {result["isin"]: {"t": result["t"], "a_p": result["a"], "a_s": result["a_v"],
                                 "b_p": result["b"], "b_s": result["b_v"]} for result in results}

    @staticmethod
    def get_ohlc_data_by_isin(ISINs, start_date, frequency):
        if frequency.startswith("da"):
            frequency = "d1"
        elif frequency.startswith("hour"):
            frequency = "h1"
        elif frequency.startswith("minute"):
            frequency = "m1"
        else:
            ValueError("Invalid frequency specified.")

        request = requests.get(
            f"https://data.lemon.markets/v1/ohlc/{frequency}?isin={concat_ISINs(ISINs)}&from={start_date}",
            headers={"Authorization": f"Bearer {market_data_key}"})
        results = request.json()["results"]

        if isinstance(ISINs, str):
            response = {ISINs: []}
        else:
            response = {isin: [] for isin in ISINs}
        for dp in results:
            response[dp["isin"]].append(
                {"x": dp["t"], "open": dp["o"], "high": dp["h"], "low": dp["l"], "close": dp["c"], "v": dp["v"]})
        return response

    @staticmethod
    def instrument_search(search):
        """Search for Name, ISIN, WKN or symbol"""
        request = requests.get(f"https://data.lemon.markets/v1/instruments",
                               data=json.dumps({"search": search}),
                               headers={"Authorization": f"Bearer {market_data_key}"})
        return request.json()
