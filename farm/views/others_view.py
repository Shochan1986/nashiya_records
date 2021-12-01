from django.shortcuts import render
from farm.models import Comment, Article
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response


@api_view(['POST'])
@permission_classes([IsAdminUser])
def createArticleComment(request, pk):
    user = request.user
    data = request.data
    article = Article.objects.get(id=pk)
    Comment.objects.create(
        article=article,
        author=user.first_name,
        text=data['text']
    )
    return Response({'detail': 'コメントが追加されました'})


@api_view(['DELETE'])
@permission_classes([IsAdminUser])
def deleteComment(request, pk):
    comment = Comment.objects.get(id=pk)
    comment.delete()  
    return Response('コメントは削除されました')
