from trading.lemon_markets.lemon_markets_wrapper import LemonMarketsWrapper
from trading.alpaca.alpaca_market_wrapper import AlpacaMarketWrapper


class UniversalMarketWrapper(AlpacaMarketWrapper):
    def __init__(self):
        super().__init__()
