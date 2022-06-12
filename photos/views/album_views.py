from photos.models import Image
from photos.serializers import (
    ChildrenImageSerializer, 
    ImageTitleSerializer,
    AlbumSerializer,
    )
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import (
    # IsAuthenticated, 
    IsAdminUser
    )
from rest_framework.response import Response
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q
from django.utils import timezone
from datetime import timedelta


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
                Q(tags__name__icontains=query) |
                Q(content_images__note__icontains=query) |
                Q(metadata__title__icontains=query) |
                Q(metadata__description__icontains=query) |
                Q(metadata__site_name__icontains=query) |
                Q(metadata__note__icontains=query) 

            )
    images = Image.objects.filter(draft=False).filter(queryset).distinct().order_by('-date', '-created')
    page = request.query_params.get('page')
    paginator = Paginator(images, 24, orphans=2)
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
    serializer = AlbumSerializer(images, many=True)
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
    images = Image.objects.filter(queryset).distinct().order_by('-date', '-created')

    page = request.query_params.get('page')
    paginator = Paginator(images, 50, orphans=2)

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
    serializer = AlbumSerializer(images, many=True)
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
    images = Image.objects.filter(draft=False) \
        .filter(tags__name=query).order_by('-date')

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
    serializer = AlbumSerializer(images, many=True)
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
def getChildrenImage(request, pk):
    image = Image.objects.get(id=pk)
    serializer = ChildrenImageSerializer(image, many=False)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([IsAdminUser])
def getIsPublicAlbum(request, pk):
    image = Image.objects.get(id=pk, draft=False)
    serializer = ChildrenImageSerializer(image, many=False)
    return Response(serializer.data)


@api_view(['POST'])
@permission_classes([IsAdminUser])
def createAlbum(request):
    album = Image.objects.create(
        title='作成中',
        author=request.user.first_name,
        date=timezone.now().date(),
        draft=True,
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
    album.special = data['special']
    album.content = data['blog']
    album.ct_is_public = data['ctIsPublic']
    album.draft = data['draft']
    tags_list = []
    tags_ids = data['tags']
    album.tags.clear()
    for tag_id in tags_ids:
        tags_list.append(tag_id)
    for elem in tags_list:
        album.tags.add(elem)
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
def getAllImages(request):
    images = Image.objects.all().order_by('-date')
    serializer = ImageTitleSerializer(images, many=True)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([IsAdminUser])
def getLatestImage(request):
    image = Image.objects.latest('id')
    serializer = ChildrenImageSerializer(image, many=False)
    return Response(serializer.data)


@api_view(['DELETE'])
@permission_classes([IsAdminUser])
def deleteAlbum(request, pk):
    album = Image.objects.get(id=pk)
    album.delete()  
    return Response('アルバムは削除されました。')


@api_view(['GET'])
@permission_classes([IsAdminUser])
def getNewAlbum(request):
    album = Image.objects.filter(draft=False) \
        .filter(created__gte=timezone.now().date()-timedelta(days=3)) \
        .order_by('-date' , '-created')[:3]
    serializer = AlbumSerializer(album, many=True)
    return Response(serializer.data)