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
from django.db.models import Q


@api_view(['GET'])
def getArticles(request):
    query = request.query_params.get('keyword')
    if query == None:
        query = ''
    queryset = (
                Q(title__icontains=query) |
                Q(task__icontains=query) |
                Q(description__icontains=query) |
                Q(pears__name__icontains=query) 
            )
    articles = Article.objects.filter(queryset).distinct()
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
    start_index = articles.start_index()
    end_index = articles.end_index()
    serializer = ArticleSerializer(articles, many=True)
    return Response(
        {
            'articles': serializer.data, 
            'page': page, 
            'pages': paginator.num_pages,
            'count': paginator.count,
            'start': start_index,
            'end': end_index,
        }
    )


@api_view(['POST'])
@permission_classes([IsAdminUser])
def createArticle(request):
    pears_list = []
    p1 = Pears.objects.get(id=1)
    pears_list.append(p1)
    article = Article.objects.create(
        title='準備中',
        task='準備中',
        description='作成中',
    )
    for element in pears_list:
        article.pears.add(element)
    article.save()
    serializer = ArticleSerializer(article, many=False)
    return Response(serializer.data)


@api_view(['GET'])
def getArticle(request, pk):
    article = Article.objects.get(id=pk)
    serializer = ArticleSerializer(article, many=False)
    return Response(serializer.data)


@api_view(['PUT'])
@permission_classes([IsAdminUser])
def updateArticle(request, pk):
    data = request.data
    article = Article.objects.get(id=pk)
    article.description = data['description']
    article.title = data['title']
    article.task = data['task']
    article.is_public = data['isPublic']
    pears_list = []
    pears_ids = data['pears']
    article.pears.clear()
    for pear_id in pears_ids:
        pears_list.append(pear_id)
    for elem in pears_list:
        article.pears.add(elem)
    article.save()
    serializer = ArticleSerializer(article, many=False)
    return Response(serializer.data)


@api_view(['DELETE'])
@permission_classes([IsAdminUser])
def deleteArticle(request, pk):
    article = Article.objects.get(id=pk)
    article.delete()  
    return Response('写真は削除されました')


@api_view(['POST'])
@permission_classes([IsAdminUser])
def createImage(request):
    images = request.FILES.getlist('images')
    for image in images:
        photo = Images()
        photo.image = image
        photo.save()
    return Response('画像がアップロードされました')


@api_view(['GET'])
@permission_classes([IsAdminUser])
def getImages(request):
    images = Images.objects.all()
    serializer = ImagesSerializer(images, many=True)
    return Response(serializer.data)


@api_view(['DELETE'])
@permission_classes([IsAdminUser])
def updateImage(request, pk):
    photo = Images.objects.get(id=pk)
    photo.image = request.FILES.get('image')
    photo.save()
    return Response('写真が更新されました')


@api_view(['DELETE'])
@permission_classes([IsAdminUser])
def deleteImage(request, pk):
    image = Images.objects.get(id=pk)
    image.delete()  
    return Response('写真は削除されました')


@api_view(['POST'])
def createPear(request):
    pear = Pears.objects.create(
        name="作成中"
    )
    serializer = PearsSerializer(pear, many=False)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([IsAdminUser])
def getPears(request):
    pears = Pears.objects.all()
    serializer = PearsSerializer(pears, many=True)
    return Response(serializer.data)


@api_view(['PUT'])
@permission_classes([IsAdminUser])
def updatePear(request, pk):
    data = request.data
    pear = Pears.objects.get(id=pk)
    pear.name = data['name']
    pear.save()
    serializer = PearsSerializer(pear, many=False)
    return Response(serializer.data)



@api_view(['DELETE'])
@permission_classes([IsAdminUser])
def deletePear(request, pk):
    pear = Pears.objects.get(id=pk)
    pear.delete()  
    return Response('写真は削除されました')
