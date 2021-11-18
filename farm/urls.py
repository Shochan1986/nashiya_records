from django.urls import path
from farm.views.user_views import (
    MyTokenObtainPairView,
    getUsers,
    getUserById,
    updateUser,
    deleteUser,
    registerUser,
)

from farm.views.article_views import (
    getArticles, 
    createArticle, 
    getArticle, 
    updateArticle, 
    deleteArticle,

    createImage,
    getImages,

    createPear,
    getPears,
)

urlpatterns = [
    path('users/login/', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
	path('users/register/', registerUser, name="register"),
    path('users/', getUsers, name="users"),
    path('users/<str:pk>/', getUserById, name="user"),
    path('users/update/<str:pk>/', updateUser, name="user-update"),
    path('users/delete/<str:pk>/', deleteUser, name="user-delete"),

    path('articles/', getArticles,),
    path('articles/create/', createArticle),
    path('articles/<str:pk>/', getArticle),
    path('articles/update/<str:pk>/', updateArticle),
    path('articles/delete/<str:pk>/', deleteArticle),

    path('images/create/', createImage),
    path('images/', getImages),

    path('pears/create/', createPear),
    path('pears/', getPears),
]