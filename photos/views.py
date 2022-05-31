from photos.models import Image, Comment, AlbumLike, Tags, ContentImage
from photos.serializers import (
    ChildrenImageSerializer, 
    CommentSerializer, 
    TagsSerializer,
    ContentImageSerializer,
    )
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import (
    # IsAuthenticated, 
    IsAdminUser
    )
from rest_framework.response import Response
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from rest_framework import status
from django.db.models import Q, Count
from django.utils import timezone
from django.utils.timezone import localtime
from datetime import timedelta, datetime


@api_view(['GET'])
@permission_classes([IsAdminUser])
def getChildrenImages(request):
    query = request.query_params.get('keyword')
    if query == None:
        query = ''
    queryset = (
                Q(title__icontains=query) |
                Q(comment__icontains=query) |
                Q(content__icontains=query) |
                Q(content_rt__icontains=query) |
                Q(comments__author__icontains=query) |
                Q(comments__text__icontains=query) |
                Q(tags__name__icontains=query) 
            )
    images = Image.objects.filter(queryset).distinct().order_by('-date')
    page = request.query_params.get('page')
    paginator = Paginator(images, 12, orphans=2)
    try:
        images = paginator.page(page)
    except PageNotAnInteger:
        images = paginator.page(1)
    except EmptyPage:
        images = paginator.page(paginator.num_pages)
    if page == None:
        page = 1
    page = int(page)
    start_index = images.start_index()
    end_index = images.end_index()
    serializer = ChildrenImageSerializer(images, many=True)
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
def getBlogImages(request):
    query = request.query_params.get('keyword')
    if query == None:
        query = ''
    queryset = (
                Q(title__icontains=query) |
                Q(comment__icontains=query) |
                Q(content__icontains=query) |
                Q(content_rt__icontains=query) |
                Q(comments__author__icontains=query) |
                Q(comments__text__icontains=query) |
                Q(tags__name__icontains=query) 
            )
    images = Image.objects.filter(ct_is_public=True).filter(queryset).distinct().order_by('-date')
    page = request.query_params.get('page')
    paginator = Paginator(images, 50, orphans=5)
    try:
        images = paginator.page(page)
    except PageNotAnInteger:
        images = paginator.page(1)
    except EmptyPage:
        images = paginator.page(paginator.num_pages)
    if page == None:
        page = 1
    page = int(page)
    start_index = images.start_index()
    end_index = images.end_index()
    serializer = ChildrenImageSerializer(images, many=True)
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
def getSpecialImages(request):
    query = request.query_params.get('keyword')
    if query == None:
        query = ''
    queryset = (
                Q(title__icontains=query) |
                Q(comment__icontains=query) |
                Q(content__icontains=query) |
                Q(content_rt__icontains=query) |
                Q(comments__author__icontains=query) |
                Q(comments__text__icontains=query) |
                Q(tags__name__icontains=query) 
            )
    images = Image.objects.filter(special=True).filter(queryset).distinct().order_by('-date')
    page = request.query_params.get('page')
    paginator = Paginator(images, 50, orphans=5)
    try:
        images = paginator.page(page)
    except PageNotAnInteger:
        images = paginator.page(1)
    except EmptyPage:
        images = paginator.page(paginator.num_pages)
    if page == None:
        page = 1
    page = int(page)
    start_index = images.start_index()
    end_index = images.end_index()
    serializer = ChildrenImageSerializer(images, many=True)
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
def getGalleryImages(request):
    query = request.query_params.get('keyword')
    if query == None:
        query = ''
    queryset = (
                Q(title__icontains=query) |
                Q(comment__icontains=query) |
                Q(content__icontains=query) |
                Q(content_rt__icontains=query) |
                Q(comments__author__icontains=query) |
                Q(comments__text__icontains=query) |
                Q(tags__name__icontains=query) 
            )
    images = Image.objects.filter(cimg_is_public=True).filter(queryset).distinct().order_by('-date')
    page = request.query_params.get('page')
    paginator = Paginator(images, 50, orphans=5)
    try:
        images = paginator.page(page)
    except PageNotAnInteger:
        images = paginator.page(1)
    except EmptyPage:
        images = paginator.page(paginator.num_pages)
    if page == None:
        page = 1
    page = int(page)
    start_index = images.start_index()
    end_index = images.end_index()
    serializer = ChildrenImageSerializer(images, many=True)
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
def getListImages(request):
    query = request.query_params.get('keyword')
    if query == None:
        query = ''
    queryset = (
                Q(title__icontains=query) |
                Q(comment__icontains=query) |
                Q(content__icontains=query) |
                Q(content_rt__icontains=query) |
                Q(comments__author__icontains=query) |
                Q(comments__text__icontains=query) |
                Q(tags__name__icontains=query) 
            )
    images = Image.objects.filter(queryset).distinct().order_by('-date')

    page = request.query_params.get('page')
    paginator = Paginator(images, 50, orphans=5)

    try:
        images = paginator.page(page)
    except PageNotAnInteger:
        images = paginator.page(1)
    except EmptyPage:
        images = paginator.page(paginator.num_pages)

    if page == None:
        page = 1
    page = int(page)
    start_index = images.start_index()
    end_index = images.end_index()
    serializer = ChildrenImageSerializer(images, many=True)
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
def getTagsPosts(request):
    query = request.query_params.get('keyword')
    if query == None:
        query = ''
    images = Image.objects.filter(tags__name=query).order_by('-date')

    page = request.query_params.get('page')
    paginator = Paginator(images, 30, orphans=3)
    try:
        images = paginator.page(page)
    except PageNotAnInteger:
        images = paginator.page(1)
    except EmptyPage:
        images = paginator.page(paginator.num_pages)
    if page == None:
        page = 1
    page = int(page)
    start_index = images.start_index()
    end_index = images.end_index()
    serializer = ChildrenImageSerializer(images, many=True)
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
def getTagsList(request):
    query = request.query_params.get('keyword')
    if query == None:
        query = ''
    queryset = Q(name__icontains=query)
    tags = Tags.objects.filter(queryset).distinct().annotate(posts=Count('images')).order_by('-posts')
    page = request.query_params.get('page')
    paginator = Paginator(tags, 25, orphans=2)
    try:
        tags = paginator.page(page)
    except PageNotAnInteger:
        tags = paginator.page(1)
    except EmptyPage:
        tags = paginator.page(paginator.num_pages)
    if page == None:
        page = 1
    page = int(page)
    start_index = tags.start_index()
    end_index = tags.end_index()
    serializer = TagsSerializer(tags, many=True)
    return Response(
        {
            'tags': serializer.data, 
            'page': page, 
            'pages': paginator.num_pages,
            'count': paginator.count,
            'start': start_index,
            'end': end_index,
        }
    )


@api_view(['GET'])
@permission_classes([IsAdminUser])
def getContentImages(request):
    c_images = ContentImage.objects.filter(image__date__gt=datetime.today()-timedelta(days=90)).order_by('-image__date')
    serializer = ContentImageSerializer(c_images, many=True)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([IsAdminUser])
def getChildrenImage(request, pk):
    image = Image.objects.get(id=pk)
    serializer = ChildrenImageSerializer(image, many=False)
    return Response(serializer.data)


@api_view(['POST'])
@permission_classes([IsAdminUser])
def createImageComment(request, pk):
    # user = request.user
    data = request.data
    image = Image.objects.get(id=pk)
    Comment.objects.create(
        image=image,
        # author=user.first_name,
        author=data['user'],
        text=data['text'],
    )
    return Response({'detail': 'コメントが追加されました'})


@api_view(['GET'])
@permission_classes([IsAdminUser])
def getComment(request, pk):
    comment = Comment.objects.get(id=pk)
    serializer = CommentSerializer(comment, many=False)
    return Response(serializer.data)


@api_view(['POST'])
@permission_classes([IsAdminUser])
def createAlbumLike(request, pk):
    user = request.user
    album_id = Image.objects.get(id=pk)
    alreadyExists = album_id.likes.filter(user=user.first_name).exists()
    if alreadyExists:
        content = {'detail': 'あなたはすでにこのアルバムに「いいね」しています'}
        return Response(content, status=status.HTTP_400_BAD_REQUEST)
    else:
        album = Image.objects.filter(id=pk)
        AlbumLike.objects.create(
            user=user.first_name,
            album=album.last(),
        )
        return Response({'detail': 'アルバムに「いいね」が追加されました'})


@api_view(['POST'])
@permission_classes([IsAdminUser])
def createContentImages(request):
    images = request.FILES.getlist('images')
    for image in images:
        instance = ContentImage()
        instance.content_image = image
        instance.save()
    return Response('挿入画像がアップロードされました')


@api_view(['POST'])
@permission_classes([IsAdminUser])
def createAlbum(request):
    album = Image.objects.create(
        title='作成中',
        date=localtime(timezone.now()).date(),
    )
    album.save()
    serializer = ChildrenImageSerializer(album, many=False)
    return Response(serializer.data)


@api_view(['PUT'])
@permission_classes([IsAdminUser])
def updateAlbum(request, pk):
    data = request.data
    album = Image.objects.get(id=pk)
    album.title = data['title']
    album.date = data['date']
    album.comment = data['note']
    album.save()
    serializer = ChildrenImageSerializer(album, many=False)
    return Response(serializer.data)


@api_view(['POST'])
@permission_classes([IsAdminUser])
def uploadAlbumImage(request):
    data = request.data
    album_id = data['album_id']
    album = Image.objects.get(id=album_id)
    album.image_one = request.FILES.get('image')
    album.save()
    return Response('画像がアップロードされました')


@api_view(['GET'])
@permission_classes([IsAdminUser])
def getContentListImages(request):
    images = ContentImage.objects.all().order_by('-id')
    page = request.query_params.get('page')
    paginator = Paginator(images, 24, orphans=4)
    try:
        images = paginator.page(page)
    except PageNotAnInteger:
        images = paginator.page(1)
    except EmptyPage:
        images = paginator.page(paginator.num_pages)
    if page == None:
        page = 1
    page = int(page)
    start_index = images.start_index()
    end_index = images.end_index()
    serializer = ContentImageSerializer(images, many=True)
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
def getAllImages(request):
    images = Image.objects.all().order_by('-created')[:25] 
    serializer = ChildrenImageSerializer(images, many=True)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([IsAdminUser])
def getLatestImage(request):
    image = Image.objects.latest('id')
    serializer = ChildrenImageSerializer(image, many=False)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([IsAdminUser])
def getContentImage(request, pk):
    content_image = ContentImage.objects.get(id=pk)
    serializer = ContentImageSerializer(content_image, many=False)
    return Response(serializer.data)


@api_view(['PUT'])
@permission_classes([IsAdminUser])
def updateContentImage(request, pk):
    data = request.data
    content_image = ContentImage.objects.get(id=pk)
    album = Image.objects.get(id=data['album'])
    content_image.image = album
    content_image.save()
    serializer = ContentImageSerializer(content_image, many=False)
    return Response(serializer.data)