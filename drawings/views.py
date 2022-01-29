from drawings.models import Drawing
from drawings.serializers import DrawingSerializer
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import (
    # IsAuthenticated, 
    IsAdminUser
    )
from rest_framework.response import Response
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
# from rest_framework import status
from django.db.models import Q


@api_view(['GET'])
@permission_classes([IsAdminUser])
def getDrawings(request):
    query = request.query_params.get('keyword')
    if query == None:
        query = ''
    queryset = (
                Q(title__icontains=query) |
                Q(description__icontains=query) 
            )
    drawings = Drawing.objects.filter(queryset).distinct().order_by('-date')
    page = request.query_params.get('page')
    paginator = Paginator(drawings, 6, orphans=1)
    try:
        drawings = paginator.page(page)
    except PageNotAnInteger:
        drawings = paginator.page(1)
    except EmptyPage:
        drawings = paginator.page(paginator.num_pages)
    if page == None:
        page = 1
    page = int(page)
    start_index = drawings.start_index()
    end_index = drawings.end_index()
    serializer = DrawingSerializer(drawings, many=True)
    return Response(
        {
            'drawings': serializer.data, 
            'page': page, 
            'pages': paginator.num_pages,
            'count': paginator.count,
            'start': start_index,
            'end': end_index,
        }
    )


@api_view(['GET'])
@permission_classes([IsAdminUser])
def getDrawing(request, pk):
    drawing = Drawing.objects.get(id=pk)
    serializer = DrawingSerializer(drawing, many=False)
    return Response(serializer.data)
