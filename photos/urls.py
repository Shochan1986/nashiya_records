from django.urls import path
from photos.views import (
    getChildrenImages,
    getChildrenImage,
    getBlogImages,
    getSpecialImages,
    getGalleryImages,
    getListImages,
    getAllImages,
    getLatestImage,

    createAlbum,
    updateAlbum,
    uploadAlbumImage,

    createContentImages,
    getContentImages,
    getContentListImages,
    getContentImage,
    updateContentImage,
    deleteContentImage,

    getTagsList,
    getTagsPosts,
    getAllTags,

    createImageComment, 
    getComment,

    createAlbumLike,
)

urlpatterns = [
    path('', getChildrenImages),
    
    path('blog/', getBlogImages),
    path('special/', getSpecialImages),
    path('list/', getListImages),
    path('latest/', getLatestImage),

    path('tags/', getTagsList),
    path('all-tags/', getAllTags),
    path('gallery/', getGalleryImages),
    path('posts/', getTagsPosts),

    path('upload/', uploadAlbumImage),

    path('create-album/', createAlbum),
    path('all-images/', getAllImages),
    path('create-images/', createContentImages),
    path('content-images/', getContentImages),
    path('content-images-list/', getContentListImages),
    path('content/<str:pk>/delete/', deleteContentImage),

    path('content/<str:pk>/', getContentImage),
    path('update/<str:pk>/', updateAlbum),

    path('<str:pk>/', getChildrenImage),

    path('images/<str:pk>/comments/', createImageComment, name="create-comment"),
    path('comments/<str:pk>/', getComment),

    path('albums/<str:pk>/album-likes/', createAlbumLike, name="create-album-like"),

    path('content/update/<str:pk>/', updateContentImage),
]