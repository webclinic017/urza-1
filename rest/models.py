from django.db import models


class Article(models.Model):
    article_id = models.IntegerField(primary_key=True)
    headline = models.CharField(max_length=128)
    author = models.CharField(max_length=128, null=True)
    url = models.CharField(max_length=255)
    text = models.TextField()
    summary = models.CharField(max_length=255, null=True)
    instrument = models.ManyToManyField(Instrument, null=True)
    created = models.DateTimeField(null=True)
    updated = models.DateTimeField(null=True)
    source = models.CharField(max_length=64)


class Instrument(models.Model):
    isin = models.CharField(max_length=12, null=True)
    symbol = models.CharField(max_length=5, null=True)
