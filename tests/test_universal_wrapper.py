import unittest
from time import sleep
from datetime import datetime, timedelta
from trading.universal_wrapper import UniversalWrapper


class UniversalWrapperTest(unittest.TestCase):
    def setUp(self):
        self.wrapper = UniversalWrapper()

    def test_get_latest_quote(self):
        result = self.wrapper.get_quote("AAPL")
        self.assertIsInstance(result[0], str)
        self.assertTrue(isinstance(result[1], (float, int)))

    def test_get_multi_quote(self):
        result = self.wrapper.get_quote(["AAPL", "GOOGL"])
        self.assertIsInstance(result, list)
        self.assertIsInstance(result[0][0], str)
        self.assertTrue(isinstance(result[0][1], (float, int)))

    def test_get_bar_data(self):
        result = self.wrapper.get_bar_data("AAPL", start_date=datetime.now() - timedelta(days=5))
        self.assertIsInstance(result, list)
        self.assertIsInstance(result[0], dict)
        self.assertIsInstance(result[0]["c"], float)
        self.assertIsInstance(result[0]["h"], float)
        self.assertIsInstance(result[0]["l"], float)
        self.assertIsInstance(result[0]["o"], float)
        self.assertIsInstance(result[0]["t"], str)

    def test_get_multi_bar_data(self):
        result = self.wrapper.get_bar_data(["AAPL", "GOOGL"], start_date=datetime.now() - timedelta(days=5))
        self.assertIsInstance(result, list)
        self.assertIsInstance(result[0], list)
        self.assertIsInstance(result[0][0], dict)
        self.assertIsInstance(result[0][0]["c"], float)
        self.assertIsInstance(result[0][0]["h"], float)
        self.assertIsInstance(result[0][0]["l"], float)
        self.assertIsInstance(result[0][0]["o"], float)
        self.assertIsInstance(result[0][0]["t"], str)

    def test_quote_stream(self):
        self.wrapper.test = None
        self.wrapper.start_quote_stream("AAPL")
        while self.wrapper.test is None:
            sleep(0.1)
        print(self.wrapper.test)
        self.wrapper.stop_quote_stream()
        self.wrapper.test = None
