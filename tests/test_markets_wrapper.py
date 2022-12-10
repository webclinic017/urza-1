import unittest
from datetime import datetime, timedelta

from trading.universal_market_wrapper import UniversalMarketWrapper


class UniversalWrapperTest(unittest.TestCase):
    def setUp(self):
        self.wrapper = UniversalMarketWrapper()

    def test_get_latest_quote(self):
        result_symbol = self.wrapper.get_quote("AAPL")
        print(result_symbol)
        self.assertIsInstance(result_symbol.keys()[0], str)
        self.assertTrue(isinstance(result_symbol.values()[0].values()[0], (float, int)))

        result_isin = self.wrapper.get_quote("US0378331005")
        print(result_isin)
        self.assertIsInstance(result_isin[0], str)
        self.assertTrue(isinstance(result_isin[1], (float, int)))

    def test_get_multi_quote(self):
        result_symbol = self.wrapper.get_quote(["AAPL", "GOOGL"])
        self.assertIsInstance(result_symbol, list)
        self.assertIsInstance(result_symbol[0][0], str)
        self.assertTrue(isinstance(result_symbol[0][1], (float, int)))

        result_isin = self.wrapper.get_quote(["US0378331005", "US02079K3059"])
        self.assertIsInstance(result_isin, list)
        self.assertIsInstance(result_isin[0][0], str)
        self.assertTrue(isinstance(result_isin[0][1], (float, int)))

    def test_get_ohlc_data(self):
        result = self.wrapper.get_ohlc_data("US0378331005",
                                            start_date=datetime.now() - timedelta(days=5),
                                            frequency="minutely")
        self.assertIsInstance(result, list)
        self.assertIsInstance(result[0], dict)
        self.assertIsInstance(result[0]["c"], float)
        self.assertIsInstance(result[0]["h"], float)
        self.assertIsInstance(result[0]["l"], float)
        self.assertIsInstance(result[0]["o"], float)
        self.assertIsInstance(result[0]["t"], str)

    def test_get_multi_ohlc_data(self):
        result = self.wrapper.get_ohlc_data(["US0378331005", "US02079K3059"],
                                            start_date=datetime.now() - timedelta(days=5),
                                            frequency="minutely")
        self.assertIsInstance(result, list)
        self.assertIsInstance(result[0], list)
        self.assertIsInstance(result[0][0], dict)
        self.assertIsInstance(result[0][0]["c"], float)
        self.assertIsInstance(result[0][0]["h"], float)
        self.assertIsInstance(result[0][0]["l"], float)
        self.assertIsInstance(result[0][0]["o"], float)
        self.assertIsInstance(result[0][0]["t"], str)

    # def test_quote_stream(self):
    #     self.wrapper.test = None
    #     self.wrapper.start_quote_stream("US0378331005")
    #     while self.wrapper.test is None:
    #         sleep(0.1)
    #     print(self.wrapper.test)
    #     self.wrapper.stop_quote_stream()
    #     self.wrapper.test = None
