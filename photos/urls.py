from django.urls import path
from photos.views import (
    getChildrenImages,
    getChildrenImage,
)


urlpatterns = [
    path('', getChildrenImages,),
    path('<str:pk>/', getChildrenImage,),
]