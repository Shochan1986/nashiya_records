from django.shortcuts import render
from farm.models import Comment, Article
from farm.serializers import CommentSerializer
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from xhtml2pdf import pisa
from django.http import HttpResponse
from django.template.loader import get_template


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


@api_view(['GET'])
#@permission_classes([IsAdminUser])
def pdfExport(request, pk):
    template_name = "article_pdf.html"
    article = Article.objects.get(id=pk)
    images = article.images.all()
    context = {"article": article, "images": images}
    template = get_template(template_name)
    html = template.render(context)
    response = HttpResponse(content_type='application/pdf')
    pdf_name = f"{article.title} {article.date}.pdf"
    response['Content-Disposition'] = f'filename="{pdf_name}"'
    pdf_status = pisa.CreatePDF(html, dest=response)
    if pdf_status.err:
        return HttpResponse('何からのエラーが発生しました。 <pre>' + html + '</pre>')
    return response
