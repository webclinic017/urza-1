from trading.alpaca.credentials import api_key, secret_key
from alpaca.trading.client import TradingClient
from alpaca.trading.requests import MarketOrderRequest, LimitOrderRequest, StopOrderRequest, StopLimitOrderRequest, \
    TrailingStopOrderRequest
from alpaca.trading.enums import OrderSide, TimeInForce


class AlpacaTradingWrapper:
    def __init__(self, paper):
        self.trading_client = TradingClient(api_key, secret_key, paper)

    def get_account_info(self):
        return self.trading_client.get_account()

    def create_order(self, symbol, quantity, side, time_in_force, order_type):
        market_order_data = MarketOrderRequest(
            symbol=symbol,
            qty=quantity,
            side=side,
            time_in_force=time_in_force
        )
