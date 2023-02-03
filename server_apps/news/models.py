from django.db import models


class Article(models.Model):
    url = models.CharField(primary_key=True)
    headline = models.CharField(max_length=255)
    html = models.TextField()
    content = models.TextField()
    date_time = models.DateTimeField(null=True)
    author = models.CharField(max_length=255, null=True)
    summary = models.CharField(null=True)
