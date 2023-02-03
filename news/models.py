from django.db import models


class Article(models.Model):
    url = models.CharField(max_length=255, primary_key=True)
    date_time = models.DateTimeField()
    headline = models.CharField(max_length=255)
    html = models.TextField()
    content = models.TextField(null=True)
    author = models.CharField(max_length=255, null=True)
    summary = models.CharField(max_length=255, null=True)
    sentiment = models.FloatField(null=True)

    class Meta:
        ordering = ["-date_time"]
        db_table = "article"
