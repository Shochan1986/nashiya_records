from django.urls import path
from farm.views.user_views import (
    MyTokenObtainPairView,
    getUsers,
    getUserById,
    updateUser,
    deleteUser,
    registerUser,

    getUserProfile,
    updateUserProfile,
)

from farm.views.article_views import (
    deleteImage,
    getArticles, 
    createArticle, 
    getArticle,
    updateArticle, 
    deleteArticle,
    getPublicArticles,

    createImage,
    getImages,
    getImage,   
    getPaginatedImages,
    updateImage,
    deleteImage,

    getPears,

    getFields,

    getCategories, 
)

from farm.views.line_views import callback

from farm.views.others_view import(
    createArticleComment, 
    updateComment,
    getComment,
    deleteComment,

    createCommentLike,
    deleteCommentLike,

    createArticleLike,
    deleteArticleLike,

    pdfExport,
    csvExport,
    )

from rest_framework_simplejwt.views import (
    TokenRefreshView,
)

urlpatterns = [
    path('users/login/', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('users/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
	path('users/register/', registerUser, name="register"),
    path('users/', getUsers, name="users"),
    path('users/<str:pk>/', getUserById, name="user"),
    path('users/update/<str:pk>/', updateUser, name="user-update"),
    path('users/delete/<str:pk>/', deleteUser, name="user-delete"),
    path('users/profile/', getUserProfile, name="users-profile"),
    path('users/profile/update/', updateUserProfile, name="users-profile-update"),

    path('articles/', getArticles,),
    path('articles/public/', getPublicArticles,),
    path('articles/create/', createArticle),
    path('articles/<str:pk>/', getArticle),
    path('articles/update/<str:pk>/', updateArticle),
    path('articles/delete/<str:pk>/', deleteArticle),

    path('articles/<str:pk>/comments/', createArticleComment, name="create-comment"),
    path('comments/<str:pk>/', getComment),
    path('comments/update/<str:pk>/', updateComment),
    path('comments/delete/<str:pk>/', deleteComment),

    path('comments/<str:pk>/comment-likes/', createCommentLike, name="create-comment-like"),
    path('comment-likes/delete/<str:pk>/', deleteCommentLike),

    path('articles/<str:pk>/article-likes/', createArticleLike, name="create-article-like"),
    path('article-likes/delete/<str:pk>/', deleteArticleLike),

    path('images/create/', createImage),
    path('images/', getImages),
    path('images/<str:pk>/', getImage),
    path('images-paginated/', getPaginatedImages),
    path('images/update/<str:pk>/', updateImage),
    path('images/delete/<str:pk>/', deleteImage),

    path('pears/', getPears),

    path('fields/', getFields),

    path('categories/', getCategories),

    path('callback/', callback, name='callback'),

    path('pdf/<str:pk>/', pdfExport, name='pdf'),
    path('csv/', csvExport, name='csv'),
]
