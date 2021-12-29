from django.urls import path
from drawings.views import (
    getDrawings,
    getDrawing,
)


urlpatterns = [
    path('drawings/', getDrawings,),
    path('drawings/<str:pk>/', getDrawing,),
]