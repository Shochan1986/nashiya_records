from django.shortcuts import render
from farm.models import Pears, Images, Field, Article
from farm.serializers import (
    PearsSerializer,
    ImagesSerializer,
    FieldSerializer,
    ArticleSerializer
)
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from rest_framework import status


@api_view(['GET'])
def getArticles(request):
    query = request.query_params.get('keyword')
    if query == None:
        query = ''

    articles = Article.objects.filter(title__icontains=query)

    page = request.query_params.get('page')
    paginator = Paginator(articles, 5)

    try:
        articles = paginator.page(page)
    except PageNotAnInteger:
        articles = paginator.page(1)
    except EmptyPage:
        articles = paginator.page(paginator.num_pages)

    if page == None:
        page = 1

    page = int(page)

    serializer = ArticleSerializer(articles, many=True)
    return Response({'articles': serializer.data, 'page': page, 'pages': paginator.num_pages})
