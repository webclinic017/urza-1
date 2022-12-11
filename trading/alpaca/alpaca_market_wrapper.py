from trading.alpaca.credentials import api_key, secret_key
from alpaca.data import StockDataStream
from alpaca.data.historical import StockHistoricalDataClient
from alpaca.data.requests import StockLatestQuoteRequest, StockBarsRequest
from alpaca.data.timeframe import TimeFrame
# Deprecated API for News Data
from alpaca_trade_api.stream import NewsDataStream
from alpaca_trade_api.common import URL


class AlpacaMarketWrapper:
    def __init__(self):
        self.quote_stream = StockDataStream(api_key, secret_key, raw_data=True)
        self.stock_client = StockHistoricalDataClient(api_key, secret_key, raw_data=True)
        # Deprecated API is needed for News Stream
        self.news_stream = NewsDataStream(api_key, secret_key,
                                          base_url=URL("wss://stream.data.alpaca.markets/v1beta1/news"),
                                          raw_data=True)

    def start_quote_stream(self, handler, symbols):
        self.quote_stream.subscribe_quotes(handler, symbols)
        self.quote_stream.run()

    def start_news_stream(self, handler, symbols=None):
        if symbols is None:
            symbols = ["*"]
        self.news_stream.subscribe_news(handler, symbols)
        # self.news_stream.run()

    def get_quote_by_symbol(self, symbols):
        request_params = StockLatestQuoteRequest(symbol_or_symbols=symbols)
        quotes = self.stock_client.get_stock_latest_quote(request_params)
        return {symbol: {"t": quotes[symbol]["t"], "a_p": quotes[symbol]["ap"], "a_s": quotes[symbol]["as"],
                         "b_p": quotes[symbol]["bp"], "b_s": quotes[symbol]["bs"]} for symbol in quotes.keys()}

    def get_ohlc_data_by_symbol(self, symbols, start_date, frequency):
        if frequency.startswith("da"):
            frequency = TimeFrame.Day
        elif frequency.startswith("month"):
            frequency = TimeFrame.Month
        elif frequency.startswith("week"):
            frequency = TimeFrame.Week
        elif frequency.startswith("hour"):
            frequency = TimeFrame.Hour
        elif frequency.startswith("minute"):
            frequency = TimeFrame.Minute
        else:
            ValueError("Invalid frequency specified.")

        request_params = StockBarsRequest(symbol_or_symbols=symbols, timeframe=frequency, start=start_date)
        results = self.stock_client.get_stock_bars(request_params)
        return results
