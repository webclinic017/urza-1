from django.contrib.auth.decorators import login_required
from django.http import JsonResponse

from server_apps.news.models import Article


@login_required
def most_recent(request, n=10):
    articles = Article.objects.all()[:n].values()
    return JsonResponse(articles)
