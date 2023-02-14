from rest_framework.decorators import api_view
from rest_framework.response import Response

from news.models import Article
from news.serializers import ArticleSerializer


@api_view["GET"]
def most_recent(request, n=10):
    articles = Article.objects.all()[:n]
    serializer = ArticleSerializer(articles)
    return Response(serializer.data)
