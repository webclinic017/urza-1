import unittest
from trading.universal_wrapper import UniversalWrapper


class UniversalWrapperTest(unittest.TestCase):
    def setUp(self):
        self.api = UniversalWrapper(sandbox=True)

    def test_get_last_tick(self):
        self.assertRaises(NotImplementedError, self.api.get_last_tick)

    def test_get_ts(self):
        google = self.api.get_ts("GOOGL", interval="60min")
        print(google)
