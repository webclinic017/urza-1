import msgpack
import websockets
from alpaca.common import APIError, RetryException
from alpaca.data.historical import StockHistoricalDataClient
from alpaca.data.requests import StockLatestQuoteRequest, StockBarsRequest
from alpaca.data.timeframe import TimeFrame


class AlpacaMarketWrapper:
    def __init__(self):
        self.close_quote_con = False

    @staticmethod
    def get_quote_by_symbol(api_key, secret_key, symbols):
        try:
            stock_client = StockHistoricalDataClient(api_key, secret_key, raw_data=True)
            request_params = StockLatestQuoteRequest(symbol_or_symbols=symbols)
            quotes = stock_client.get_stock_latest_quote(request_params)
        except APIError:
            return {"status": "error", "error_type": "authentication"}
        except RetryException:
            return {"status": "error", "error_type": "connection"}

        return {symbol: {"t": quotes[symbol]["t"], "a_p": quotes[symbol]["ap"], "a_s": quotes[symbol]["as"],
                         "b_p": quotes[symbol]["bp"], "b_s": quotes[symbol]["bs"]} for symbol in quotes.keys()}

    @staticmethod
    def get_ohlc_data_by_symbol(api_key, secret_key, symbols, start_date, frequency):
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
            frequency = TimeFrame.Day

        try:
            stock_client = StockHistoricalDataClient(api_key, secret_key, raw_data=True)
            request_params = StockBarsRequest(symbol_or_symbols=symbols, timeframe=frequency, start=start_date)
            results = stock_client.get_stock_bars(request_params)
        except APIError:
            return {"status": "error", "error_type": "authentication"}
        except RetryException:
            return {"status": "error", "error_type": "connection"}

        if isinstance(symbols, str):
            response = {symbols: []}
        else:
            response = {symbol: [] for symbol in symbols}
        for symbol in results:
            for dp in results[symbol]:
                response[symbol].append(
                    {"t": dp["t"], "open": dp["o"], "high": dp["h"], "low": dp["l"], "close": dp["c"], "v": dp["v"]})
        return response

    async def start_quote_stream(self, api_key, secret_key, handler, quotes):
        uri = "wss://stream.data.alpaca.markets/v2/iex"
        async with websockets.connect(uri, extra_headers={"Content-Type": "application/msgpack"}) as ws:
            r = await ws.recv()
            await handler(msgpack.unpackb(r)[0]["T"])

            # authenticate
            await ws.send(msgpack.packb({'action': 'auth', 'key': api_key, 'secret': secret_key}))
            r = await ws.recv()
            await handler(msgpack.unpackb(r)[0]["T"])

            # If only a single quote was given
            if isinstance(quotes, str):
                quotes = [quotes]
            # subscribe
            await ws.send(msgpack.packb({"action": "subscribe", "quotes": quotes}))
            r = await ws.recv()
            await handler(msgpack.unpackb(r)[0]["T"])

            while not self.close_quote_con:
                r = await ws.recv()
                await handler(msgpack.unpackb(r))

    async def stop_quote_stream(self):
        self.close_quote_con = True
