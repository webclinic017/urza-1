import unittest
from trading.lemon_markets.helpers import *

class HelpersTest(unittest.TestCase):

    def test_format_currency(self):
        self.assertEqual(format_currency(5), 50000)

    def test_create_idempotency(self):
        self.assertNotEqual(create_idempotency(), create_idempotency())

    def test_concat_ISINs(self):
        self.assertEqual(concat_ISINs(["US0378331005", "US02079K3059"]), "US0378331005,US02079K3059")
        self.assertEqual(concat_ISINs("US0378331005"), "US0378331005")
