from photos.models import (
    Image, Comment, Reply, Metadata
    )
from photos.serializers import (
    MetadataSerializer,
    )
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import (
    # IsAuthenticated, 
    IsAdminUser
    )
from rest_framework.response import Response
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q
import metadata_parser



@api_view(['POST'])
@permission_classes([IsAdminUser])
def createMetadata(request):
    data = request.data
    try:
        album = Image.objects.get(id=data['album'])
    except Image.DoesNotExist:
        album = None
    try:
        comment = Comment.objects.get(id=data['comment'])
    except Comment.DoesNotExist:
        comment = None
    try:
        reply = Reply.objects.get(id=data['reply'])
    except Reply.DoesNotExist:
        reply = None
    instance = Metadata()
    instance.album = album
    instance.author = request.user.first_name
    instance.comment = comment
    instance.reply = reply
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
    serializer = MetadataSerializer(instance, many=False)
    return Response(serializer.data)


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
    try:
        comment = Comment.objects.get(id=data['comment'])
    except Comment.DoesNotExist:
        comment = None
    try:
        reply = Reply.objects.get(id=data['reply'])
    except Reply.DoesNotExist:
        reply = None
    meta.album = album
    meta.comment = comment
    meta.reply = reply
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
