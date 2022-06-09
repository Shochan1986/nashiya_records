from photos.models import (
    Image, Comment, AlbumLike, 
    Reply, Tags
    )
from photos.serializers import (
    CommentSerializer, 
    TagsSerializer,
    ReplySerializer,
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
def getTagsList(request):
    query = request.query_params.get('keyword')
    if query == None:
        query = ''
    queryset = Q(name__icontains=query)
    tags = Tags.objects.filter(images__draft=False) \
        .filter(queryset).distinct().annotate(posts=Count('images')).order_by('-posts')
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


@api_view(['GET'])
@permission_classes([IsAdminUser])
def getAllTags(request):
    tags = Tags.objects.all().annotate(posts=Count('images')).order_by('-posts')
    serializer = TagsSerializer(tags, many=True)
    return Response(serializer.data)


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
    comments = Comment.objects.filter(image__draft=False) \
        .filter(created__gte=timezone.now().date()-timedelta(days=2)) \
        .order_by('-created')[:3]
    serializer = CommentSerializer(comments, many=True)
    return Response(serializer.data)


@api_view(['POST'])
@permission_classes([IsAdminUser])
def createCommentReply(request, pk):
    data = request.data
    comment = Comment.objects.get(id=pk)
    Reply.objects.create(
        comment=comment,
        author=data['user'],
        text=data['text'],
    )
    return Response({'detail': '返信が追加されました'})


@api_view(['GET'])
@permission_classes([IsAdminUser])
def getReply(request, pk):
    reply = Reply.objects.get(id=pk)
    serializer = ReplySerializer(reply, many=False)
    return Response(serializer.data)