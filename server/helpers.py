from django.core.cache import caches


def get_trader_cache(request):
    """Return Cached Trader Data.
    :param request: used for getting ID from logged-in User.
    :return: Trader Model
    """
    trader_id = request.user.id
    return caches[trader_id]
