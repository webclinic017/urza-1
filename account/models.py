from django.contrib.auth.base_user import AbstractBaseUser
from django.db import models


# This is the global User object. Every specific subtype of User for each app has a reference to the global User
class GlobalUser(AbstractBaseUser):
    email = models.EmailField(unique=True)
    
    USERNAME_FIELD = "email"
    EMAIL_FIELD = "email"
    REQUIRED_FIELDS = ["email", "password"]


class Instrument(models.Model):
    isin = models.CharField(max_length=12, null=True)
    symbol = models.CharField(max_length=5, null=True)


class AlpacaCredentials(models.Model):
    paper = models.BooleanField()
    api_key = models.CharField(max_length=64)
    secret_key = models.CharField(max_length=64)


class LemonMarketsCredentials(models.Model):
    paper = models.BooleanField()
    market_data_key = models.CharField()
    paper_trading_key = models.CharField()
    trading_key = models.CharField(null=True)
    pin = models.IntegerField(max_length=16, null=True)


class TradingUser(models.Model):
    global_user = models.OneToOneField(GlobalUser, on_delete=models.CASCADE)
    alpaca_config = models.OneToOneField(AlpacaCredentials, on_delete=models.SET_NULL, null=True)
    lemon_markets_config = models.OneToOneField(LemonMarketsCredentials, on_delete=models.SET_NULL, null=True)


class Trade(models.Model):
    trade_date = models.DateTimeField()
    instrument = models.ForeignKey(Instrument, on_delete=models.SET_NULL)
    article = models.ForeignKey("news.Article", on_delete=models.SET_NULL)
    trader = models.ForeignKey(TradingUser, on_delete=models.SET_NULL)
