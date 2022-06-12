from photos.models import (
    Image, Comment,
    Reply, ContentImage,
    )
from photos.serializers import (
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
from datetime import timedelta


@api_view(['GET'])
@permission_classes([IsAdminUser])
def getContentImages(request):
    c_images = ContentImage.objects.filter(image__draft=False) \
        .filter(image__date__gt=timezone.now().date()-timedelta(days=120)) \
        .annotate(num_comments=Count('comment')) \
        .filter(num_comments=0) \
        .annotate(num_replies=Count('reply')) \
        .filter(num_replies=0) \
        .order_by('-image__date', '-image__created')
    serializer = ContentImageSerializer(c_images, many=True)
    return Response(serializer.data)


@api_view(['POST'])
@permission_classes([IsAdminUser])
def createContentImages(request):
    data = request.data
    try:
        album = Image.objects.get(id=data['album'])
    except Image.DoesNotExist:
        album = None
        pass
    try:
        comment = Comment.objects.get(id=data['comment'])
    except Comment.DoesNotExist:
        comment = None
        pass
    try:
        reply = Reply.objects.get(id=data['reply'])
    except Reply.DoesNotExist:
        reply = None
        pass
    images = request.FILES.getlist('images')
    
    for photo in images:
        instance = ContentImage()
        if album:
            instance.image = album
        if comment:
            instance.comment = comment
        if reply:
            instance.reply = reply
        instance.note = data['note']
        instance.content_image = photo
        request = request
        instance.save()
    return Response('挿入画像がアップロードされました')


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
    images = ContentImage.objects.filter(queryset).distinct().order_by('-created', '-id') 
        # .annotate(num_comments=Count('comment')) \
        # .filter(num_comments=0) \
        # .annotate(num_replies=Count('reply')) \
        # .filter(num_replies=0) \
        
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


@api_view(['DELETE'])
@permission_classes([IsAdminUser])
def deleteContentImage(request, pk):
    image = ContentImage.objects.get(id=pk)
    image.delete()  
    return Response('写真は削除されました。')