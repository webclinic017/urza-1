from trading.alpha_vantage_wrapper.alpha_vantage_wrapper import AlphaVantageWrapper


class UniversalWrapper(AlphaVantageWrapper):
    def __init__(self, sandbox):
        super().__init__(sandbox)
