from django.urls import path
from photos.views import (
    getChildrenImages,
    getChildrenImage,
    getBlogImages,

    createImageComment, 
    updateComment,
    getComment,
    deleteComment,

    createCommentLike,
    deleteCommentLike,
)

urlpatterns = [
    path('', getChildrenImages),
    path('blog/', getBlogImages),
    path('<str:pk>/', getChildrenImage),

    path('images/<str:pk>/comments/', createImageComment, name="create-comment"),
    path('comments/<str:pk>/', getComment),
    path('comments/update/<str:pk>/', updateComment),
    path('comments/delete/<str:pk>/', deleteComment),

    path('comments/<str:pk>/comment-likes/', createCommentLike, name="create-comment-like"),
    path('comment-likes/delete/<str:pk>/', deleteCommentLike),
]