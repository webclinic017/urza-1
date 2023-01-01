import asyncio

from channels.layers import get_channel_layer

from market.market_wrapper import MarketWrapper


async def start_alpaca_news_stream():
    async def handler(data):
        # Redirect to Django Channel
        channel_layer = get_channel_layer()
        await channel_layer.group_send("market", {"type": "news_article", "data": data})

    wrapper = MarketWrapper()

    loop = asyncio.get_event_loop()
    task = loop.create_task(wrapper.start_news_stream(handler))
