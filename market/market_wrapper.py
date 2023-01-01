from market.alpaca.alpaca_market import AlpacaMarketWrapper
from market.lemon_markets.lemon_market import LemonMarketWrapper


class MarketWrapper(LemonMarketWrapper, AlpacaMarketWrapper):

    @staticmethod
    def get_quote(symbols_or_isins):
        """
        :param symbols_or_isins: "AAPL" or "US0378331005" or ["AAPL", "GOOGL"] or  ["US0378331005", "US02079K3059"]
        :return: [{'AAPL': {'t': '2022-12-09T21:00:18.731241505Z', 'a_p': 0, 'a_s': 0, 'b_p': 0, 'b_s': 0}}, ...]
        """
        if isinstance(symbols_or_isins, str):
            if len(symbols_or_isins) == 12:
                return MarketWrapper.get_quote_by_isin(symbols_or_isins)
            else:
                return MarketWrapper.get_quote_by_symbol(symbols_or_isins)
        else:
            if len(symbols_or_isins[0]) == 12:
                return MarketWrapper.get_quote_by_isin(symbols_or_isins)
            else:
                return MarketWrapper.get_quote_by_symbol(symbols_or_isins)

    @staticmethod
    def get_ohlc_data(symbols_or_isins, start_date, frequency):
        """
        :param symbols_or_isins: "AAPL" or "US0378331005" or ["AAPL", "GOOGL"] or  ["US0378331005", "US02079K3059"]
        :param start_date: datetime.isoformat()
        :param frequency: "minutly", "hourly", "daily"
        :return: {'AAPL': [{'t': '2022-12-07T05:00:00Z', 'o': 142.19, ...}]}
        """
        if isinstance(symbols_or_isins, str):
            if len(symbols_or_isins) == 12:
                return MarketWrapper.get_ohlc_data_by_isin(symbols_or_isins, start_date, frequency)
            else:
                return MarketWrapper.get_ohlc_data_by_symbol(symbols_or_isins, start_date, frequency)
        else:
            if len(symbols_or_isins[0]) == 12:
                return MarketWrapper.get_ohlc_data_by_isin(symbols_or_isins, start_date, frequency)
            else:
                return MarketWrapper.get_ohlc_data_by_symbol(symbols_or_isins, start_date, frequency)
