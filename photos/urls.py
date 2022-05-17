from django.urls import path
from photos.views import (
    getChildrenImages,
    getChildrenImage,
    getBlogImages,
    getSpecialImages,
    getListImages,
    getLastYearImages,

    createImageComment, 
    updateComment,
    getComment,
    deleteComment,

    createAlbumLike,
)

urlpatterns = [
    path('', getChildrenImages),
    path('blog/', getBlogImages),
    path('special/', getSpecialImages),
    path('list/', getListImages),
    path('last-year/', getLastYearImages),

    path('<str:pk>/', getChildrenImage),

    path('images/<str:pk>/comments/', createImageComment, name="create-comment"),
    path('comments/<str:pk>/', getComment),
    path('comments/update/<str:pk>/', updateComment),
    path('comments/delete/<str:pk>/', deleteComment),

    path('albums/<str:pk>/album-likes/', createAlbumLike, name="create-album-like"),
]