import msgpack
from alpaca.data.historical import StockHistoricalDataClient
from alpaca.data.requests import StockLatestQuoteRequest, StockBarsRequest
from alpaca.data.timeframe import TimeFrame

from trading.alpaca.credentials import api_key, secret_key


class AlpacaMarketWrapper:
    def __init__(self):
        self.stock_client = StockHistoricalDataClient(api_key, secret_key, raw_data=True)

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


async def stream():
    uri = "wss://stream.data.alpaca.markets/v1beta1/news"
    async with websockets.connect(uri, extra_headers={"Content-Type": "application/msgpack"}) as ws:
        r = await ws.recv()
        print(msgpack.unpackb(r))
        await ws.send(msgpack.packb({'action': 'auth', 'key': api_key, 'secret': secret_key}))
        r = await ws.recv()
        print(msgpack.unpackb(r))
        await ws.send(msgpack.packb({"action": "subscribe", "news": ["*"]}))
        r = await ws.recv()
        print(msgpack.unpackb(r))
        while True:
            r = await ws.recv()
            print(msgpack.unpackb(r))


asyncio.run(stream())
