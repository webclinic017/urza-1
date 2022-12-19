from django.db import models


class Articles(models.Model):
    id = models.IntegerField(primary_key=True)
    headline = models.CharField(max_length=128)
    author = models.CharField(max_length=128)
    url = models.CharField(max_length=255)
    text = models.TextField()
