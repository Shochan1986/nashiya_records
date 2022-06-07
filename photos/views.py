from photos.models import Image, Comment, AlbumLike, Tags, ContentImage, Metadata
from photos.serializers import (
    ChildrenImageSerializer, 
    CommentSerializer, 
    TagsSerializer,
    ContentImageSerializer,
    ImageTitleSerializer,
    AlbumSerializer,
    MetadataSerializer,
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
import metadata_parser


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
    images = Image.objects.filter(queryset).distinct().order_by('-date', '-created')
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
    images = Image.objects.filter(queryset).distinct().order_by('-date')

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
    images = Image.objects.filter(tags__name=query).order_by('-date')

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
    c_images = ContentImage.objects.filter(image__date__gt=datetime.today()-timedelta(days=120)).order_by('-image__date', '-image__created')
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
    data = request.data
    try:
        album = Image.objects.get(id=data['album'])
    except Image.DoesNotExist:
        album = None
        pass
    images = request.FILES.getlist('images')
    if album:
        for photo in images:
            instance = ContentImage()
            instance.image = album
            instance.content_image = photo
            request = request
            instance.save()
    else:
        for photo in images:
            instance = ContentImage()
            instance.content_image = photo
            request = request
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
    album.special = data['special']
    album.content = data['blog']
    album.ct_is_public = data['ctIsPublic']
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
def getContentListImages(request):
    query = request.query_params.get('keyword')
    if query == None:
        query = ''
    queryset = (
        Q(image__title__icontains=query) |
        Q(content_image__icontains=query) 
    )
    images = ContentImage.objects.filter(queryset).distinct().order_by('-id')
    page = request.query_params.get('page')
    paginator = Paginator(images, 48, orphans=4)
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
    images = Image.objects.all().order_by('-date')
    serializer = ImageTitleSerializer(images, many=True)
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
    try:
        album = Image.objects.get(id=data['album'])
    except Image.DoesNotExist:
        album = None
    if album:
        content_image.image = album
        content_image.note = data['note']
        content_image.save()
    else:
        content_image.image = None
        content_image.note = data['note']
        content_image.save()
    serializer = ContentImageSerializer(content_image, many=False)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([IsAdminUser])
def getAllTags(request):
    tags = Tags.objects.all().annotate(posts=Count('images')).order_by('-posts')
    serializer = TagsSerializer(tags, many=True)
    return Response(serializer.data)


@api_view(['DELETE'])
@permission_classes([IsAdminUser])
def deleteContentImage(request, pk):
    image = ContentImage.objects.get(id=pk)
    image.delete()  
    return Response('写真は削除されました。')


@api_view(['GET'])
@permission_classes([IsAdminUser])
def email_send(request, pk):
    image = Image.objects.get(id=pk)
    try:
        image.email_push(request) 
        return Response(f'「{image.title}」がEメールで送信されました。')
    except:
        content = {'detail': f'「{image.title}」をEメールで送信できませんでした。'}
        return Response(content, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([IsAdminUser])
def line_send(request, pk):
    image = Image.objects.get(id=pk)
    try:
        image.line_push(request) 
        return Response(f'「{image.title}」がLINEで送信されました。')
    except:
        content = {'detail': f'「{image.title}」をLINEで送信できませんでした。'}
        return Response(content, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([IsAdminUser])
def createMetadata(request):
    data = request.data
    try:
        album = Image.objects.get(id=data['album'])
    except Image.DoesNotExist:
        album = None

    instance = Metadata()
    instance.album = album
    instance.note = data['note']
    instance.family = data['family']
    instance.site_url = data['site_url']
    page = metadata_parser.MetadataParser(data['site_url'])
    instance.title = page.get_metadatas('title')[0]
    if page.get_metadatas('site_name') is not None:
        instance.site_name = page.get_metadatas('site_name')[0]
    else:
        pass
    if page.get_metadatas('image') is not None:
        instance.image_url = page.get_metadatas('image')[0]
    else:
        pass
    if page.get_metadatas('description') is not None:
        instance.description = page.get_metadatas('description')[0]
    else:
        pass
    instance.save()
    return Response('メタデータがアップロードされました')


@api_view(['GET'])
@permission_classes([IsAdminUser])
def getMetadata(request):
    query = request.query_params.get('keyword')
    if query == None:
        query = ''
    queryset = (
        Q(site_url__icontains=query) |
        Q(site_name__icontains=query) |
        Q(title__icontains=query) |
        Q(note__icontains=query) |
        Q(description__icontains=query) |
        Q(album__title__icontains=query) 
    )
    data = Metadata.objects.filter(queryset).distinct().order_by('-created')
    page = request.query_params.get('page')
    paginator = Paginator(
        data,
        # 2, 
        24, 
        orphans=4
    )
    try:
        data = paginator.page(page)
    except PageNotAnInteger:
        data = paginator.page(1)
    except EmptyPage:
        data = paginator.page(paginator.num_pages)
    if page == None:
        page = 1
    page = int(page)
    start_index = data.start_index()
    end_index = data.end_index()
    serializer = MetadataSerializer(data, many=True)
    return Response(
        {
            'data': serializer.data, 
            'page': page, 
            'pages': paginator.num_pages,
            'count': paginator.count,
            'start': start_index,
            'end': end_index,
        }
    )


@api_view(['GET'])
@permission_classes([IsAdminUser])
def getSingleMetadata(request, pk):
    meta = Metadata.objects.get(id=pk)
    serializer = MetadataSerializer(meta, many=False)
    return Response(serializer.data)


@api_view(['DELETE'])
@permission_classes([IsAdminUser])
def deleteMetadata(request, pk):
    meta = Metadata.objects.get(id=pk)
    meta.delete()  
    return Response('メタデータは削除されました。')


@api_view(['PUT'])
@permission_classes([IsAdminUser])
def updateMetadata(request, pk):
    data = request.data
    meta = Metadata.objects.get(id=pk)
    try:
        album = Image.objects.get(id=data['album'])
    except Image.DoesNotExist:
        album = None
    meta.album = album
    meta.note = data['note']
    meta.family = data['family']
    meta.site_url = data['site_url']
    page = metadata_parser.MetadataParser(data['site_url'])
    meta.title = page.get_metadatas('title')[0]
    if page.get_metadatas('site_name') is not None:
        meta.site_name = page.get_metadatas('site_name')[0]
    else:
        meta.site_name = ''
    if meta.image_url:
        if page.get_metadatas('image') is not None:
            meta.image_url = page.get_metadatas('image')[0]
        else:
            meta.image_url = data['image_url']
    else:
        meta.image_url = data['image_url']
    if page.get_metadatas('description') is not None:
        meta.description = page.get_metadatas('description')[0]
    else:
        meta.description = ''
    meta.save()
    serializer = MetadataSerializer(meta, many=False)
    return Response(serializer.data)


@api_view(['DELETE'])
@permission_classes([IsAdminUser])
def deleteAlbum(request, pk):
    album = Image.objects.get(id=pk)
    album.delete()  
    return Response('アルバムは削除されました。')


@api_view(['POST'])
@permission_classes([IsAdminUser])
def createTag(request):
    data = request.data
    tag = Tags()
    tag.name = data['name']
    tag.save()
    serializer = TagsSerializer(tag, many=False)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([IsAdminUser])
def getSingleTag(request, pk):
    tag = Tags.objects.get(id=pk)
    serializer = TagsSerializer(tag, many=False)
    return Response(serializer.data)


@api_view(['DELETE'])
@permission_classes([IsAdminUser])
def deleteTag(request, pk):
    tag = Tags.objects.get(id=pk)
    tag.delete()  
    return Response('タグが削除されました。')


@api_view(['PUT'])
@permission_classes([IsAdminUser])
def updateTag(request, pk):
    data = request.data
    tag = Tags.objects.get(id=pk)
    tag.name = data['name']
    tag.save()
    serializer = TagsSerializer(tag, many=False)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([IsAdminUser])
def getLatestTag(request):
    tag = Tags.objects.latest('id')
    serializer = TagsSerializer(tag, many=False)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([IsAdminUser])
def getNewComments(request):
    comments = Comment.objects \
        .filter(created__gte=datetime.today()-timedelta(days=2)) \
        .order_by('-created')[:3]
    serializer = CommentSerializer(comments, many=True)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([IsAdminUser])
def getNewAlbum(request):
    album = Image.objects.filter(created__gte=datetime.today()-timedelta(days=3)) \
        .order_by('-date' , '-created')[:3]
    serializer = AlbumSerializer(album, many=True)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([IsAdminUser])
def getMetaFamily(request):
    query = request.query_params.get('keyword')
    if query == None:
        query = ''
    queryset = (
        Q(site_url__icontains=query) |
        Q(site_name__icontains=query) |
        Q(title__icontains=query) |
        Q(note__icontains=query) |
        Q(description__icontains=query) |
        Q(album__title__icontains=query) 
    )
    data = Metadata.objects.filter(family=True).filter(queryset).distinct().order_by('-album__date', '-album__created')
    page = request.query_params.get('page')
    paginator = Paginator(
        data, 
        # 2,
        24, 
        orphans=2,
    )
    try:
        data = paginator.page(page)
    except PageNotAnInteger:
        data = paginator.page(1)
    except EmptyPage:
        data = paginator.page(paginator.num_pages)
    if page == None:
        page = 1
    page = int(page)
    start_index = data.start_index()
    end_index = data.end_index()
    serializer = MetadataSerializer(data, many=True)
    return Response(
        {
            'data': serializer.data, 
            'page': page, 
            'pages': paginator.num_pages,
            'count': paginator.count,
            'start': start_index,
            'end': end_index,
        }
    )