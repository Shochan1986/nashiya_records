from django.urls import path
from drawings.views import (
    getDrawings,
    getDrawing,

    createDrawingComment, 
    updateComment,
    getComment,
    deleteComment,

    createCommentLike,
    deleteCommentLike,
)


urlpatterns = [
    path('', getDrawings,),
    path('<str:pk>/', getDrawing,),

    path('drawings/<str:pk>/comments/', createDrawingComment, name="create-comment"),
    path('comments/<str:pk>/', getComment),
    path('comments/update/<str:pk>/', updateComment),
    path('comments/delete/<str:pk>/', deleteComment),

    path('comments/<str:pk>/comment-likes/', createCommentLike, name="create-comment-like"),
    path('comment-likes/delete/<str:pk>/', deleteCommentLike),
]