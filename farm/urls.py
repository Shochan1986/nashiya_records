from django.urls import path, include
from farm.views import getArticles

urlpatterns = [
    path('', getArticles,),
]