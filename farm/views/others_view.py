from django.shortcuts import render
from farm.models import Comment, Article
from farm.serializers import CommentSerializer
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from xhtml2pdf import pisa
from django.http import HttpResponse
from django.template.loader import get_template
from django.contrib.admin.views.decorators import staff_member_required
from django.utils.html import linebreaks, urlize
from django_pandas.io import read_frame
from django.utils import timezone
import urllib, csv


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


@staff_member_required
def pdfExport(request, pk):
    template_name = "article_pdf.html"
    article = Article.objects.get(id=pk)
    pears = ",".join(map(str, article.pears.all())) 
    fields = ",".join(map(str, article.fields.all())) 
    images = article.images.all()
    text = urlize(linebreaks(article.description))
    context = {
        "article": article, 
        "pears": pears,
        "fields": fields,
        "images": images,
        "text": text,
        }
    template = get_template(template_name)
    html = template.render(context)
    response = HttpResponse(content_type='application/pdf')
    pdf_name = f"{article.title} {article.date}.pdf"
    response['Content-Disposition'] = f'filename="{pdf_name}"'
    pdf_status = pisa.CreatePDF(html, dest=response)
    if pdf_status.err:
        return HttpResponse('何からのエラーが発生しました。 <pre>' + html + '</pre>')
    return response


@staff_member_required
def csvExport(request):
    articles = Article.objects.all().order_by('-created')
    date = timezone.now().date()
    response = HttpResponse(content_type='text/csv;charset=CP932')
    filename = urllib.parse.quote((f'梨屋さん日報アプリ {date}.csv').encode("utf8"))
    response['Content-Disposition'] = 'filename*=UTF-8\'\'{}'.format(filename)
    writer = csv.writer(response)
    writer.writerow([
        '番号',
        '作業内容',
        '作業日付',
        '作成者',
        '分類',
        '作業場所',
        '品種',
        '詳細',
        '完了',
        '作成日',
        '完了日',
        '画像URL',
    ])

    index = 0
    for index, article in enumerate(articles, start=1):
        writer.writerow([
            str(index),
            article.title,
            article.date.strftime('%Y{0}%m{1}%d{2}').format(*'年月日'),
            article.user.first_name,
            article.category.name,
            '、 '.join([elem.name for elem in article.fields.all()]), 
            '、 '.join([elem.name for elem in article.pears.all()]), 
            article.description,
            article.get_is_public_display(),
            article.created.strftime('%Y{0}%m{1}%d{2}').format(*'年月日'),
            article.published_at.strftime('%Y{0}%m{1}%d{2}').format(*'年月日'),
            '\n'.join([elem.url for elem in article.images.all()]), 
        ])
    return response
