from trading.lemon_markets.lemon_markets_wrapper import LemonMarketsWrapper
from trading.alpaca.alpaca_wrapper import AlpacaWrapper


class UniversalWrapper(AlpacaWrapper):
    def __init__(self):
        super().__init__()
