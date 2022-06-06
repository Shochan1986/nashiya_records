from django.urls import path
from photos.views import (
    deleteAlbum,
    deleteMetadata,
    deleteTag,
    
    getChildrenImages,
    getChildrenImage,
    getMetaFamily,
    getListImages,
    getAllImages,
    getLatestImage,
    deleteAlbum,
    getNewAlbum,

    createAlbum,
    updateAlbum,
    uploadAlbumImage,

    createContentImages,
    getContentImages,
    getContentListImages,
    getContentImage,
    updateContentImage,
    deleteContentImage,

    updateMetadata,
    deleteMetadata,
    getSingleMetadata,

    getTagsList,
    getTagsPosts,
    getAllTags,
    createTag,
    getSingleTag,
    updateTag,
    deleteTag,
    getLatestTag,

    createImageComment, 
    getComment,

    createAlbumLike,

    email_send,
    line_send,

    createMetadata,
    getMetadata,
    getLatestMetadata,
    getMetaFamily,  
)

urlpatterns = [
    path('', getChildrenImages),
    
    path('list/', getListImages),

    path('latest/', getLatestImage),
    path('tags-latest/', getLatestTag),
    path('meta-latest/', getLatestMetadata),
    path('new/', getNewAlbum),

    path('tags/', getTagsList),
    path('all-tags/', getAllTags),
    path('tags-create/', createTag),

    path('posts/', getTagsPosts),

    path('upload/', uploadAlbumImage),

    path('meta-create/', createMetadata),
    path('meta/', getMetadata),
    path('meta-family/', getMetaFamily),

    path('create-album/', createAlbum),
    path('all-images/', getAllImages),
    path('create-images/', createContentImages),
    path('content-images/', getContentImages),
    path('content-images-list/', getContentListImages),

    path('meta/<str:pk>/', getSingleMetadata),
    path('meta/<str:pk>/update/', updateMetadata),
    path('meta/<str:pk>/delete/', deleteMetadata),

    path('content/<str:pk>/', getContentImage),
    path('content/update/<str:pk>/', updateContentImage),
    path('content/<str:pk>/delete/', deleteContentImage),

    path('tags/<str:pk>/', getSingleTag),
    path('tags/<str:pk>/update/', updateTag),
    path('tags/<str:pk>/delete/', deleteTag),

    path('update/<str:pk>/', updateAlbum),
    path('delete/<str:pk>/', deleteAlbum),

    path('<str:pk>/', getChildrenImage),

    path('images/<str:pk>/comments/', createImageComment, name="create-comment"),
    path('comments/<str:pk>/', getComment),

    path('albums/<str:pk>/album-likes/', createAlbumLike, name="create-album-like"),

    path('email/<str:pk>/', email_send),
    path('line/<str:pk>/', line_send),
]