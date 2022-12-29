import asyncio
from datetime import datetime, timedelta

import pytest

from trading.lemon_markets.helpers import *
from trading.market_wrapper import MarketWrapper


@pytest.fixture
def wrapper():
    return MarketWrapper()


class TestMarketWrapper:

    def test_get_latest_quote(self, wrapper):
        symbol_result = wrapper.get_quote("AAPL")
        isin_result = wrapper.get_quote("US0378331005")

        # Check datetime
        assert isinstance(symbol_result["AAPL"]["t"], str)
        assert isinstance(isin_result["US0378331005"]["t"], str)
        # Check ask price
        assert isinstance(symbol_result["AAPL"]["a_p"], (float, int))
        assert isinstance(isin_result["US0378331005"]["a_p"], (float, int))

    def test_get_multi_quote(self, wrapper):
        symbol_result = wrapper.get_quote(["AAPL", "GOOGL"])
        isin_result = wrapper.get_quote(["US0378331005", "US02079K3059"])

        # Check datetime
        assert isinstance(symbol_result["GOOGL"]["t"], str)
        assert isinstance(isin_result["US02079K3059"]["t"], str)
        # Check ask price
        assert isinstance(symbol_result["GOOGL"]["a_p"], (float, int))
        assert isinstance(isin_result["US02079K3059"]["a_p"], (float, int))

    def test_get_ohlc_data(self, wrapper):
        symbol_result = wrapper.get_ohlc_data("AAPL",
                                              start_date=datetime.now() - timedelta(days=5),
                                              frequency="daily")
        isin_result = wrapper.get_ohlc_data("US0378331005",
                                            start_date=datetime.now() - timedelta(days=5),
                                            frequency="daily")

        assert isinstance(symbol_result["AAPL"], list)
        assert isinstance(symbol_result["AAPL"][0], dict)
        assert isinstance(symbol_result["AAPL"][0]["t"], str)
        assert isinstance(symbol_result["AAPL"][0]["o"], float)

        assert isinstance(isin_result["US0378331005"], list)
        assert isinstance(isin_result["US0378331005"][0], dict)
        assert isinstance(isin_result["US0378331005"][0]["t"], str)
        assert isinstance(isin_result["US0378331005"][0]["o"], float)

    def test_get_multi_ohlc_data(self, wrapper):
        symbol_result = wrapper.get_ohlc_data(["AAPL", "GOOGL"],
                                              start_date=datetime.now() - timedelta(days=5),
                                              frequency="daily")
        isin_result = wrapper.get_ohlc_data(["US0378331005", "US02079K3059"],
                                            start_date=datetime.now() - timedelta(days=5),
                                            frequency="daily")

        assert isinstance(symbol_result["GOOGL"], list)
        assert isinstance(symbol_result["GOOGL"][0], dict)
        assert isinstance(symbol_result["GOOGL"][0]["t"], str)
        assert isinstance(symbol_result["GOOGL"][0]["o"], float)

        assert isinstance(isin_result["US02079K3059"], list)
        assert isinstance(isin_result["US02079K3059"][0], dict)
        assert isinstance(isin_result["US02079K3059"][0]["t"], str)
        assert isinstance(isin_result["US02079K3059"][0]["o"], float)


@pytest.mark.asyncio
class TestWebsocketStreams:

    async def test_quote_stream(self, wrapper):
        async def handler(data):
            assert data == "success" or data == "subscription"

        loop = asyncio.get_event_loop()
        task = loop.create_task(wrapper.start_quote_stream(handler, "AAPL"))
        await asyncio.sleep(1)
        await wrapper.stop_news_stream()

    async def test_news_stream(self, wrapper):
        async def handler(data):
            assert data == "success" or data == "subscription"

        loop = asyncio.get_event_loop()
        task = loop.create_task(wrapper.start_news_stream(handler))
        await asyncio.sleep(1)
        await wrapper.stop_news_stream()


class TestHelpers:

    def test_format_currency(self):
        assert format_currency(5), 50000

    def test_create_idempotency(self):
        assert create_idempotency(), create_idempotency()

    def test_concat_ISINs(self):
        assert concat_ISINs(["US0378331005", "US02079K3059"]), "US0378331005,US02079K3059"
        assert concat_ISINs("US0378331005"), "US0378331005"
