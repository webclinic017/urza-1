from django.db import models


class Instrument(models.Model):
    isin = models.CharField(max_length=12, null=True)
    symbol = models.CharField(max_length=5, null=True)


class Article(models.Model):
    article_id = models.IntegerField(primary_key=True)
    headline = models.CharField(max_length=255)
    author = models.CharField(max_length=255, null=True)
    url = models.CharField()
    text = models.TextField()
    summary = models.CharField(null=True)
    instrument = models.ManyToManyField(Instrument)
    created = models.DateTimeField(null=True)
    updated = models.DateTimeField(null=True)
    source = models.CharField(max_length=64)


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


class Trader(models.Model):
    name = models.CharField(max_length=64)
    alpaca_config = models.OneToOneField(AlpacaCredentials, on_delete=models.CASCADE)
    lemon_markets_config = models.OneToOneField(LemonMarketsCredentials, on_delete=models.CASCADE)


class Trade(models.Model):
    trade_date = models.DateTimeField()
    instrument = models.ForeignKey(Instrument, on_delete=models.SET_NULL)
    article = models.ForeignKey(Article, on_delete=models.SET_NULL)
    trader = models.ForeignKey(Trader, on_delete=models.SET_NULL)
