from trading.lemon_markets.lemon_markets_wrapper import LemonMarketsWrapper
from trading.alpaca.alpaca_market_wrapper import AlpacaMarketWrapper


class UniversalMarketWrapper(LemonMarketsWrapper, AlpacaMarketWrapper):
    def __init__(self):
        LemonMarketsWrapper.__init__(self)
        AlpacaMarketWrapper.__init__(self)

    def get_quote(self, symbols_or_isins, price="ask"):
        if isinstance(symbols_or_isins, str):
            if len(symbols_or_isins) == 12:
                return self.get_quote_by_isin(symbols_or_isins, price)
            else:
                return self.get_quote_by_symbol(symbols_or_isins, price)
        else:
            if len(symbols_or_isins[0]) == 12:
                return self.get_quote_by_isin(symbols_or_isins, price)
            else:
                return self.get_quote_by_symbol(symbols_or_isins, price)

    def get_ohlc_data(self, symbols_or_isins, start_date, frequency):
        if isinstance(symbols_or_isins, str):
            if len(symbols_or_isins) == 12:
                return self.get_ohlc_data_by_isin(symbols_or_isins, start_date, frequency)
            else:
                return self.get_ohlc_data_by_symbol(symbols_or_isins, start_date, frequency)
        else:
            if len(symbols_or_isins[0]) == 12:
                return self.get_ohlc_data_by_isin(symbols_or_isins, start_date, frequency)
            else:
                return self.get_ohlc_data_by_symbol(symbols_or_isins, start_date, frequency)

