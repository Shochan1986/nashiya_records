from farm.models import Category, Pears, Images, Fields, Article
from farm.serializers import (
    PearsSerializer,
    ImagesSerializer,
    FieldsSerializer,
    ArticleSerializer,
    CategorySerializer
)
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from rest_framework import status
from django.db.models import Q
from django.utils import timezone
from django.contrib.auth.models import User


@api_view(['GET'])
@permission_classes([IsAdminUser])
def getArticles(request):
    query = request.query_params.get('keyword')
    if query == None:
        query = ''
    queryset = (
                Q(title__icontains=query) |
                Q(description__icontains=query) |
                Q(pears__name__icontains=query) | 
                Q(fields__name__icontains=query) | 
                Q(images__comment__icontains=query) |
                Q(user__first_name__icontains=query)
            )
    articles = Article.objects.filter(queryset).distinct()
    page = request.query_params.get('page')
    paginator = Paginator(articles, 6)
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


@api_view(['GET'])
@permission_classes([IsAdminUser])
def getPublicArticles(request):
    query = request.query_params.get('keyword')
    if query == None:
        query = ''
    queryset = (
                Q(title__icontains=query) |
                Q(description__icontains=query) |
                Q(pears__name__icontains=query) | 
                Q(fields__name__icontains=query) |
                Q(images__comment__icontains=query) | 
                Q(comments__author__icontains=query) |
                Q(comments__text__icontains=query) |
                Q(user__first_name__icontains=query) 
            )
    articles = Article.objects.filter(is_public=True).filter(queryset).distinct()
    page = request.query_params.get('page')
    paginator = Paginator(articles, 6)
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
    user = User.objects.get(id=1)
    cat = Category.objects.get(id=1)
    pears_list = []
    p1 = Pears.objects.get(id=1)
    pears_list.append(p1)
    fields_list = []
    f1 = Fields.objects.get(id=1)
    fields_list.append(f1)
    article = Article.objects.create(
        user=user,
        title='準備中',
        date=timezone.now().date(),
        category=cat,
        description='詳細は後ほど。。。',
    )
    for elem_p in pears_list:
        article.pears.add(elem_p)
    for elem_f in fields_list:
        article.fields.add(elem_f)
    article.save()
    serializer = ArticleSerializer(article, many=False)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([IsAdminUser])
def getArticle(request, pk):
    article = Article.objects.get(id=pk)
    serializer = ArticleSerializer(article, many=False)
    return Response(serializer.data)


@api_view(['PUT'])
@permission_classes([IsAdminUser])
def updateArticle(request, pk):
    data = request.data
    article = Article.objects.get(id=pk)
    article.user = User.objects.get(id=data['user'])
    article.description = data['description']
    article.title = data['title']
    article.date = data['date']
    cat = Category.objects.get(id=data['category'])
    article.category = cat
    article.is_public = data['isPublic']
    pears_list = []
    pears_ids = data['pears']
    article.pears.clear()
    for pear_id in pears_ids:
        pears_list.append(pear_id)
    for elem_p in pears_list:
        article.pears.add(elem_p)
    fields_list = []
    fields_ids = data['fields']
    article.fields.clear()
    for field_id in fields_ids:
        fields_list.append(field_id)
    for elem_f in fields_list:
        article.fields.add(elem_f)
    images_list = []
    images_ids = data['images']
    article.images.clear()
    for image_id in images_ids:
        images_list.append(image_id)
    for elem_i in images_list:
        article.images.add(elem_i)
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
    # photo = request.FILES.get('image')
    # image = Images(image=photo)
    # image.save()
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


@api_view(['GET'])
@permission_classes([IsAdminUser])
def getPaginatedImages(request):
    query = request.query_params.get('keyword')
    if query == None:
        query = ''
    queryset = (
                Q(comment__icontains=query) |
                Q(author__icontains=query)  
            )
    images = Images.objects.filter(queryset).distinct()
    page = request.query_params.get('page')
    paginator = Paginator(images, 12, orphans=3)
    try:
        images = paginator.page(page)
    except PageNotAnInteger:
        images = paginator.page(1)
    except EmptyPage:
        images = paginator.page(paginator.num_pages)
    if page == None:
        page = 1
    page = int(page)
    serializer = ImagesSerializer(images, many=True)
    start_index = images.start_index()
    end_index = images.end_index()
    return Response(
        {
            'images': serializer.data, 
            'page': page, 
            'pages': paginator.num_pages,
            'count': paginator.count,
            'start': start_index,
            'end': end_index,
        }
    )


@api_view(['GET'])
@permission_classes([IsAdminUser])
def getImage(request, pk):
    image = Images.objects.get(id=pk)
    serializer = ImagesSerializer(image, many=False)
    return Response(serializer.data)


@api_view(['PUT'])
@permission_classes([IsAdminUser])
def updateImage(request, pk):
    user = request.user
    data = request.data
    image = Images.objects.get(id=pk)
    image.author = user.first_name
    image.comment = data['comment']
    image.save()
    serializer = ImagesSerializer(image, many=False)
    return Response(serializer.data)


@api_view(['DELETE'])
@permission_classes([IsAdminUser])
def deleteImage(request, pk):
    image = Images.objects.get(id=pk)
    image.delete()  
    return Response('写真は削除されました')


@api_view(['GET'])
@permission_classes([IsAdminUser])
def getPears(request):
    pears = Pears.objects.all()
    serializer = PearsSerializer(pears, many=True)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([IsAdminUser])
def getFields(request):
    fields = Fields.objects.all()
    serializer = FieldsSerializer(fields, many=True)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([IsAdminUser])
def getCategories(request):
    categories = Category.objects.all()
    serializer = CategorySerializer(categories, many=True)
    return Response(serializer.data)
