from trading.lemon_markets.lemon_markets_wrapper import LemonMarketsWrapper
from trading.alpaca.alpaca_market_wrapper import AlpacaMarketWrapper


class UniversalMarketWrapper(LemonMarketsWrapper, AlpacaMarketWrapper):
    def __init__(self):
        LemonMarketsWrapper.__init__(self)
        AlpacaMarketWrapper.__init__(self)

    def get_quote(self, symbol_or_ISIN, price="ask"):
        if len(symbol_or_ISIN) == 12:
            return self.get_quote_by_isin(symbol_or_ISIN, price)
        else:
            return self.get_quote_by_symbol(symbol_or_ISIN, price)
