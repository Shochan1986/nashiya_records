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
    df = read_frame(articles, 
        fieldnames=[
            'id',
            'title', 
            'date', 
            'user', 
            'category', 
            # 'fields',
            # 'pears',
            'description',
            'is_public',
            'created',
            'published_at',
            ]
    )
    column_labels = [
        'ID',
        '作業内容',
        '作業日付',
        '作成者Eメール',
        '分類',
        # '作業場所',
        # '品種',
        '詳細',
        '完了',
        '作成日',
        '完了日',
    ]
    df.columns = column_labels
    df['作成日'] = df['作成日'].dt.strftime('%Y-%m-%d')
    df['完了'] = df['完了'] * 1
    df['完了'] = df['完了'].replace({
        1: '完了',
        0: '下書き',
    })
    df['完了日'] = df['完了日'].dt.strftime('%Y-%m-%d')
    date = timezone.now().date()
    response = HttpResponse(content_type='text/csv;charset=CP932')
    response['Content-Disposition'] = f'attachment; filename=covid19_梨屋さん日報アプリ {date}.csv'
    df.to_csv(path_or_buf=response, encoding='utf-8-sig', index=None)
    return response
