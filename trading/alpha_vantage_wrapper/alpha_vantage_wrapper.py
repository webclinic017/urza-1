from trading.alpha_vantage_wrapper.credentials import api_key
from alpha_vantage.timeseries import TimeSeries


class AlphaVantageWrapper:
    def __init__(self, sandbox):
        self.ts = TimeSeries(key=api_key, output_format='pandas')

    def get_last_tick(self, symbol):
        raise NotImplementedError("Alpha Vantage does not offer real time trading data.")

    def get_ts(self, symbol, interval, metadata=False):
        data, metadata = self.ts.get_intraday(symbol=symbol, interval=interval)
        if metadata:
            return data, metadata
        return data
