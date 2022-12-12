import asyncio

import msgpack
import websockets
from alpaca.data.historical import StockHistoricalDataClient
from alpaca.data.requests import StockLatestQuoteRequest, StockBarsRequest
from alpaca.data.timeframe import TimeFrame

from trading.alpaca.credentials import api_key, secret_key


class AlpacaMarketWrapper:
    def __init__(self):
        self.stock_client = StockHistoricalDataClient(api_key, secret_key, raw_data=True)
        self.close_quote_con = False
        self.close_news_con = False

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

    async def _quote_stream(self, handler, quotes):
        uri = "wss://stream.data.alpaca.markets/v2/iex"
        async with websockets.connect(uri, extra_headers={"Content-Type": "application/msgpack"}) as ws:
            r = await ws.recv()
            print(msgpack.unpackb(r))
            await ws.send(msgpack.packb({'action': 'auth', 'key': api_key, 'secret': secret_key}))
            r = await ws.recv()
            print(msgpack.unpackb(r))
            # If only a single quote was given
            if isinstance(quotes, str):
                quotes = [quotes]
            await ws.send(msgpack.packb({"action": "subscribe", "quotes": quotes}))
            r = await ws.recv()
            print(msgpack.unpackb(r))
            while not self.close_quote_con:
                r = await ws.recv()
                await handler(r)

    async def _news_stream(self, handler):
        async with websockets.connect("wss://stream.data.alpaca.markets/v1beta1/news",
                                      extra_headers={"Content-Type": "application/msgpack"}) as ws:
            r = await ws.recv()
            print(msgpack.unpackb(r))
            await ws.send(msgpack.packb({'action': 'auth', 'key': api_key, 'secret': secret_key}))
            r = await ws.recv()
            print(msgpack.unpackb(r))
            await ws.send(msgpack.packb({"action": "subscribe", "news": ["*"]}))
            r = await ws.recv()
            print(msgpack.unpackb(r))
            while not self.close_news_con:
                r = await ws.recv()
                await handler(r)

    async def start_quote_stream(self, handler, quotes):
        asyncio.run(self._quote_stream(handler, quotes))

    async def start_news_stream(self, handler):
        asyncio.run(self._news_stream(handler))

    async def stop_quote_stream(self):
        self.close_quote_con = True

    async def stop_news_stream(self):
        self.close_news_con = True
