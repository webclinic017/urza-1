from rest_framework.decorators import api_view
from rest_framework.response import Response

from market_wrapper.market_wrapper import MarketWrapper


@api_view(['GET'])
def get_quote(request, symbols_or_isins):
    return Response(MarketWrapper.get_quote(symbols_or_isins))


@api_view(['GET'])
def get_ohlc_data(request, symbols_or_isins, start_date, frequency):
    return Response(MarketWrapper.get_ohlc_data(symbols_or_isins))
