import unittest
from datetime import datetime, timedelta

from trading.universal_market_wrapper import UniversalMarketWrapper


class UniversalWrapperTest(unittest.TestCase):
    def setUp(self):
        self.wrapper = UniversalMarketWrapper()

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

    # def test_quote_stream(self):
    #     self.wrapper.test = None
    #     self.wrapper.start_quote_stream("US0378331005")
    #     while self.wrapper.test is None:
    #         sleep(0.1)
    #     print(self.wrapper.test)
    #     self.wrapper.stop_quote_stream()
    #     self.wrapper.test = None
