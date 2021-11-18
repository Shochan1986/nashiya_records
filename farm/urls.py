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
    deleteArticle
)

urlpatterns = [
    path('login/', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
	path('register/', registerUser, name="register"),
    path('', getUsers, name="users"),
    path('<str:pk>/', getUserById, name="user"),
    path('update/<str:pk>/', updateUser, name="user-update"),
    path('delete/<str:pk>/', deleteUser, name="user-delete"),

    path('', getArticles,),
    path('create/', createArticle),
    path('<str:pk>/', getArticle),
    path('<str:pk>/update/', updateArticle),
    path('<str:pk>/delete/', deleteArticle),
]