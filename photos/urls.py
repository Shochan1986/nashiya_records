from django.urls import path
from photos.views import (
    getChildrenImages,
    getChildrenImage,
    getBlogImages,
    getSpecialImages,
    getGalleryImages,
    getListImages,

    createAlbum,
    updateAlbum,
    uploadAlbumImage,

    createContentImages,
    getContentImages,
    getContentListImages,

    getTagsList,
    getTagsPosts,

    createImageComment, 
    getComment,

    createAlbumLike,
)

urlpatterns = [
    path('', getChildrenImages),
    
    path('blog/', getBlogImages),
    path('special/', getSpecialImages),
    path('list/', getListImages),

    path('tags/', getTagsList),
    path('gallery/', getGalleryImages),
    path('posts/', getTagsPosts),

    path('create-album/', createAlbum),
    path('create-images/', createContentImages),
    path('content-images/', getContentImages),
    path('content-images-list/', getContentListImages),
    path('update/<str:pk>/', updateAlbum),
    path('upload/', uploadAlbumImage),

    path('<str:pk>/', getChildrenImage),

    path('images/<str:pk>/comments/', createImageComment, name="create-comment"),
    path('comments/<str:pk>/', getComment),

    path('albums/<str:pk>/album-likes/', createAlbumLike, name="create-album-like"),
]