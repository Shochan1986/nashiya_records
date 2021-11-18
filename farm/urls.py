from django.urls import path
from farm.views.article_views import (
    getArticles, 
    createArticle, 
    getArticle, 
    updateArticle, 
    deleteArticle
)

urlpatterns = [
    path('', getArticles,),
    path('create/', createArticle),
    path('<int:pk>/', getArticle),
    path('<int:pk>/update/', updateArticle),
    path('<int:pk>/delete/', deleteArticle),
]