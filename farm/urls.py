from django.urls import path, include
from farm.views import getArticles, createArticle, getArticle

urlpatterns = [
    path('', getArticles,),
    path('create/', createArticle),
    path('<int:pk>/', getArticle)
]