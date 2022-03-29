from photos.models import Image, Comment, CommentLike
from photos.serializers import ChildrenImageSerializer, CommentSerializer
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import (
    # IsAuthenticated, 
    IsAdminUser
    )
from rest_framework.response import Response
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from rest_framework import status
from django.db.models import Q
from django.views.generic.base import View


@api_view(['GET'])
@permission_classes([IsAdminUser])
def getChildrenImages(request):
    query = request.query_params.get('keyword')
    if query == None:
        query = ''
    queryset = (
                Q(title__icontains=query) |
                Q(comment__icontains=query) 
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
                Q(comment__icontains=query) 
            )
    images = Image.objects.filter(ct_is_public=True).filter(queryset).distinct().order_by('-date')
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
def getChildrenImage(request, pk):
    image = Image.objects.get(id=pk)
    serializer = ChildrenImageSerializer(image, many=False)
    return Response(serializer.data)


@api_view(['POST'])
@permission_classes([IsAdminUser])
def createImageComment(request, pk):
    user = request.user
    data = request.data
    image = Image.objects.get(id=pk)
    Comment.objects.create(
        image=image,
        author=user.first_name,
        text=data['text']
    )
    return Response({'detail': 'コメントが追加されました'})


@api_view(['GET'])
@permission_classes([IsAdminUser])
def getComment(request, pk):
    comment = Comment.objects.get(id=pk)
    serializer = CommentSerializer(comment, many=False)
    return Response(serializer.data)


@api_view(['PUT'])
@permission_classes([IsAdminUser])
def updateComment(request, pk):
    data = request.data
    comment = Comment.objects.get(id=pk)
    comment.text = data['text']
    comment.save()
    serializer = CommentSerializer(comment, many=False)
    return Response(serializer.data)


@api_view(['DELETE'])
@permission_classes([IsAdminUser])
def deleteComment(request, pk):
    comment = Comment.objects.get(id=pk)
    comment.delete()  
    return Response('コメントは削除されました')


@api_view(['POST'])
@permission_classes([IsAdminUser])
def createCommentLike(request, pk):
    user = request.user
    comment_id = Comment.objects.get(id=pk)
    alreadyExists = comment_id.likes.filter(user=user.first_name).exists()
    if alreadyExists:
        content = {'detail': 'あなたはすでにこのコメントに「いいね」しています'}
        return Response(content, status=status.HTTP_400_BAD_REQUEST)
    else:
        comment = Comment.objects.filter(id=pk)
        CommentLike.objects.create(
            user=user.first_name,
            comment=comment.last(),
        )
        return Response({'detail': 'コメントに「いいね」が追加されました'})


@api_view(['DELETE'])
@permission_classes([IsAdminUser])
def deleteCommentLike(request, pk):
    like = CommentLike.objects.get(id=pk)
    like.delete()  
    return Response('コメントの「いいね」は削除されました')