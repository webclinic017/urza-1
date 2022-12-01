import unittest
from trading.universal_wrapper import UniversalWrapper


class UniversalWrapperTest(unittest.TestCase):
    def setUp(self):
        self.api = UniversalWrapper()

    def test_get_latest_quote(self):
        google = self.api.get_latest_quote("US02079K3059")
        print(google)

    def test_get_timeseries(self):
        google = self.api.get_timeseries("US02079K3059")
        print(google)
