from django.contrib.auth.decorators import login_required
from django.http import JsonResponse

from market_wrapper.market_wrapper import MarketWrapper


@login_required
def get_quote(request, symbols_or_isins):
    return JsonResponse(MarketWrapper.get_quote(symbols_or_isins))


@login_required
def get_ohlc_data(request, symbols_or_isins, start_date, frequency):
    return JsonResponse(MarketWrapper.get_ohlc_data(symbols_or_isins))


@login_required
def instrument_search(request, search):
    return JsonResponse(MarketWrapper.instrument_search(search))
