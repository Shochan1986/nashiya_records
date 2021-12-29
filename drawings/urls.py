from django.urls import path
from drawings.views import (
    getDrawings,
    getDrawing,
)


urlpatterns = [
    path('', getDrawings,),
    path('<str:pk>/', getDrawing,),
]