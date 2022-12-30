import json

from django.contrib.auth.decorators import login_required
from django.http import JsonResponse

from trading.market_wrapper import MarketWrapper


@login_required
def get_quote(request, symbols_or_isins):
    return JsonResponse(json.dumps(MarketWrapper.get_quote(symbols_or_isins)))


@login_required
def get_ohlc_data(request, symbols_or_isins, start_date, frequency):
    return JsonResponse(json.dumps(MarketWrapper.get_quote(symbols_or_isins)))
