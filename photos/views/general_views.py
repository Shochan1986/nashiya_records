from photos.models import (
    Image, Comment, AlbumLike, ContentImage,
    Reply, Tags, CommentLike, ReplyLike, Video,
    )
from photos.serializers import (
    CommentSerializer, 
    TagsSerializer,
    ReplySerializer,
    VideoSerializer,
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
from xhtml2pdf import pisa
from django.http import HttpResponse
from django.template.loader import get_template
from django.http import FileResponse


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


@api_view(['POST'])
@permission_classes([IsAdminUser])
def createImageComment(request, pk):
    data = request.data
    image = Image.objects.get(id=pk)
    Comment.objects.create(
        image=image,
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
    return Response('コメントが削除されました。')


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


@api_view(['POST'])
@permission_classes([IsAdminUser])
def createReplyLike(request, pk):
    user = request.user
    reply_id = Reply.objects.get(id=pk)
    alreadyExists = reply_id.likes.filter(user=user.first_name).exists()
    if alreadyExists:
        content = {'detail': 'あなたはすでにこの返信に「いいね」しています'}
        return Response(content, status=status.HTTP_400_BAD_REQUEST)
    else:
        reply = Reply.objects.filter(id=pk)
        ReplyLike.objects.create(
            user=user.first_name,
            reply=reply.last(),
        )
        return Response({'detail': '返信に「いいね」が追加されました'})


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
        content = {'detail': f'「{image.title}」をEメールで送信できませんでした。\n \
        少なくとも１枚の画像をサムネイルに指定してください。'}
        return Response(content, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([IsAdminUser])
def line_send(request, pk):
    image = Image.objects.get(id=pk)
    try:
        image.line_push(request) 
        return Response(f'「{image.title}」がLINEで送信されました。')
    except:
        content = {'detail': f'「{image.title}」をLINEで送信できませんでした。\n \
        少なくとも１枚の画像をサムネイルに指定してください。'}
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


@api_view(['PUT'])
@permission_classes([IsAdminUser])
def updateReply(request, pk):
    data = request.data
    reply = Reply.objects.get(id=pk)
    reply.text = data['text']
    reply.save()
    serializer = ReplySerializer(reply, many=False)
    return Response(serializer.data)


@api_view(['DELETE'])
@permission_classes([IsAdminUser])
def deleteReply(request, pk):
    reply = Reply.objects.get(id=pk)
    reply.delete()  
    return Response('返信が削除されました。')


@api_view(['GET'])
@permission_classes([IsAdminUser])
def pdfExport(request, pk):
    template_name = "photos/pdf.html"
    album = Image.objects.get(id=pk)
    images = ContentImage.objects.filter(image__id=pk, comment=None, reply=None)
    note = album.comment
    context = {
        "album": album, 
        "note": note,
        "images": images,
        }
    template = get_template(template_name)
    html = template.render(context)
    response = HttpResponse(content_type='application/pdf')
    pdf_name = f"{album.title} {album.date}.pdf"
    response['Content-Disposition'] = f'attachment; filename="{pdf_name}"'
    pdf_status = pisa.CreatePDF(html, dest=response)
    if pdf_status.err:
        return HttpResponse('何からのエラーが発生しました。 <pre>' + html + '</pre>')
    return response


@api_view(['POST'])
@permission_classes([IsAdminUser])
def uploadVideo(request):
    data = request.data
    video = Video()
    video.album = Image.objects.get(id=data['album_id'])
    video.author_id = request.user.id
    video.author_name = request.user.first_name
    video.title = data['title']
    video.video = request.FILES.get('video')
    video.save()
    serializer = VideoSerializer(video, many=False)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([IsAdminUser])
def getVideos(request):
    videos = Video.objects.all()
    serializer = VideoSerializer(videos, many=True)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([IsAdminUser])
def getSingleVideo(request, pk):
    video = Video.objects.get(id=pk)
    serializer = VideoSerializer(video, many=False)
    return Response(serializer.data)


@api_view(['PUT'])
@permission_classes([IsAdminUser])
def updateVideo(request, pk):
    data = request.data
    video = Video.objects.get(id=pk)
    video.album = Image.objects.get(id=data['album_id'])
    video.author_id = request.user.id
    video.author_name = request.user.first_name
    video.title = data['title']
    video.video = request.FILES.get('video')
    video.save()
    serializer = VideoSerializer(video, many=False)
    return Response(serializer.data)


@api_view(['POST'])
@permission_classes([IsAdminUser])
def uploadVideoThumbnail(request, pk):
    video = Video.objects.get(id=pk)
    video.thumbnail = request.FILES.get('thumbnail')
    video.save()
    serializer = VideoSerializer(video, many=False)
    return Response(serializer.data)


@api_view(['DELETE'])
@permission_classes([IsAdminUser])
def deleteVideo(request, pk):
    video = Video.objects.get(id=pk)
    video.delete()  
    return Response('動画が削除されました。')
