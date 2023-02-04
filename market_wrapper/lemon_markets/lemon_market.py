import json

import requests

from market_wrapper.lemon_markets.utils import concat_ISINs


class LemonMarketWrapper:

    @staticmethod
    def get_quote_by_isin(market_key, ISINs):
        ISINs = concat_ISINs(ISINs)

        try:
            request = requests.get(f"https://data.lemon.markets/v1/quotes/latest?isin={ISINs}",
                                   headers={"Authorization": f"Bearer {market_key}"})
        except requests.exceptions.RequestException:
            return {"status": "error", "error_type": "connection"}
        results = request.json()
        if results.get("status") == "error":
            return {"status": "error", "error_type": "authentication"}

        results = results["results"]
        response = {result["isin"]: {"t": result["t"], "a_p": result["a"], "a_s": result["a_v"],
                                     "b_p": result["b"], "b_s": result["b_v"]} for result in results}
        return response

    @staticmethod
    def get_ohlc_data_by_isin(market_key, ISINs, start_date, frequency):
        if frequency.startswith("da"):
            frequency = "d1"
        elif frequency.startswith("hour"):
            frequency = "h1"
        elif frequency.startswith("minute"):
            frequency = "m1"
        else:
            frequency = "d1"

        try:
            request = requests.get(
                f"https://data.lemon.markets/v1/ohlc/{frequency}?isin={concat_ISINs(ISINs)}&from={start_date}",
                headers={"Authorization": f"Bearer {market_key}"})
        except requests.exceptions.RequestException:
            return {"status": "error", "error_type": "connection"}

        results = request.json()
        if results.get("status") == "error":
            return {"status": "error", "error_type": "authentication"}
        results = results["results"]

        if isinstance(ISINs, str):
            response = {ISINs: []}
        else:
            response = {isin: [] for isin in ISINs}
        for dp in results:
            response[dp["isin"]].append(
                {"t": dp["t"], "open": dp["o"], "high": dp["h"], "low": dp["l"], "close": dp["c"], "v": dp["v"]})
        return response

    @staticmethod
    def instrument_search(market_key, search):
        """Search for Name, ISIN, WKN or symbol"""
        try:
            request = requests.get(f"https://data.lemon.markets/v1/instruments",
                                   data=json.dumps({"search": search}),
                                   headers={"Authorization": f"Bearer {market_key}"})
        except requests.exceptions.RequestException:
            return {"status": "error", "error_type": "connection"}
        return request.json()
