import asyncio
import unittest
from datetime import datetime, timedelta

from trading.lemon_markets.helpers import *
from trading.market_wrapper import MarketWrapper


class MarketWrapperTest(unittest.TestCase):
    def setUp(self):
        self.wrapper = MarketWrapper()

    def test_get_latest_quote(self):
        symbol_result = self.wrapper.get_quote("AAPL")
        isin_result = self.wrapper.get_quote("US0378331005")

        # Check datetime
        self.assertIsInstance(symbol_result["AAPL"]["t"], str)
        self.assertIsInstance(isin_result["US0378331005"]["t"], str)
        # Check ask price
        self.assertTrue(isinstance(symbol_result["AAPL"]["a_p"], (float, int)))
        self.assertTrue(isinstance(isin_result["US0378331005"]["a_p"], (float, int)))

    def test_get_multi_quote(self):
        symbol_result = self.wrapper.get_quote(["AAPL", "GOOGL"])
        isin_result = self.wrapper.get_quote(["US0378331005", "US02079K3059"])

        # Check datetime
        self.assertIsInstance(symbol_result["GOOGL"]["t"], str)
        self.assertIsInstance(isin_result["US02079K3059"]["t"], str)
        # Check ask price
        self.assertTrue(isinstance(symbol_result["GOOGL"]["a_p"], (float, int)))
        self.assertTrue(isinstance(isin_result["US02079K3059"]["a_p"], (float, int)))

    def test_get_ohlc_data(self):
        symbol_result = self.wrapper.get_ohlc_data("AAPL",
                                                   start_date=datetime.now() - timedelta(days=5),
                                                   frequency="daily")
        isin_result = self.wrapper.get_ohlc_data("US0378331005",
                                                 start_date=datetime.now() - timedelta(days=5),
                                                 frequency="daily")

        self.assertIsInstance(symbol_result["AAPL"], list)
        self.assertIsInstance(symbol_result["AAPL"][0], dict)
        self.assertIsInstance(symbol_result["AAPL"][0]["t"], str)
        self.assertIsInstance(symbol_result["AAPL"][0]["o"], float)

        self.assertIsInstance(isin_result["US0378331005"], list)
        self.assertIsInstance(isin_result["US0378331005"][0], dict)
        self.assertIsInstance(isin_result["US0378331005"][0]["t"], str)
        self.assertIsInstance(isin_result["US0378331005"][0]["o"], float)

    def test_get_multi_ohlc_data(self):
        symbol_result = self.wrapper.get_ohlc_data(["AAPL", "GOOGL"],
                                                   start_date=datetime.now() - timedelta(days=5),
                                                   frequency="daily")
        isin_result = self.wrapper.get_ohlc_data(["US0378331005", "US02079K3059"],
                                                 start_date=datetime.now() - timedelta(days=5),
                                                 frequency="daily")

        self.assertIsInstance(symbol_result["GOOGL"], list)
        self.assertIsInstance(symbol_result["GOOGL"][0], dict)
        self.assertIsInstance(symbol_result["GOOGL"][0]["t"], str)
        self.assertIsInstance(symbol_result["GOOGL"][0]["o"], float)

        self.assertIsInstance(isin_result["US02079K3059"], list)
        self.assertIsInstance(isin_result["US02079K3059"][0], dict)
        self.assertIsInstance(isin_result["US02079K3059"][0]["t"], str)
        self.assertIsInstance(isin_result["US02079K3059"][0]["o"], float)


class TestWebsocketStreams(unittest.IsolatedAsyncioTestCase):
    def setUp(self):
        self.wrapper = MarketWrapper()

    async def test_quote_stream(self):
        async def handler(data):
            self.assertTrue(data == "success" or data == "subscription")

        loop = asyncio.get_event_loop()
        task = loop.create_task(self.wrapper.start_quote_stream(handler, "AAPL"))
        await asyncio.sleep(1)
        await self.wrapper.stop_news_stream()

    async def test_news_stream(self):
        async def handler(data):
            self.assertTrue(data == "success" or data == "subscription")

        loop = asyncio.get_event_loop()
        task = loop.create_task(self.wrapper.start_news_stream(handler))
        await asyncio.sleep(1)
        await self.wrapper.stop_news_stream()


class HelpersTest(unittest.TestCase):

    def test_format_currency(self):
        self.assertEqual(format_currency(5), 50000)

    def test_create_idempotency(self):
        self.assertNotEqual(create_idempotency(), create_idempotency())

    def test_concat_ISINs(self):
        self.assertEqual(concat_ISINs(["US0378331005", "US02079K3059"]), "US0378331005,US02079K3059")
        self.assertEqual(concat_ISINs("US0378331005"), "US0378331005")
