import imp
from django.urls import path
from farm.views.others_view import pdfExport
from photos.views.album_views import (
    deleteAlbum,

    getChildrenImages,
    getChildrenImage,

    getListImages,
    getAllImages,
    getLatestImage,
    deleteAlbum,
    getNewAlbum,
    getIsPublicAlbum,

    createAlbum,
    updateAlbum,
    uploadAlbumImage,

    getTagsPosts,
)
from photos.views.general_views import (
    deleteTag,

    createCommentReply,
    getReply,
    updateReply,
    deleteReply,

    getTagsList,
    getAllTags,
    createTag,
    getSingleTag,
    updateTag,
    deleteTag,
    getLatestTag,

    createImageComment,
    getComment,
    getNewComments,
    updateComment,
    deleteComment,

    createAlbumLike,
    createCommentLike,
    createReplyLike,

    email_send,
    line_send, 

    pdfExport,

    uploadVideo,
)

from photos.views.content_views import (
    createContentImages,
    getContentImages,
    getContentListImages,
    getContentImage,
    updateContentImage,
    deleteContentImage,
)

from photos.views.meta_views import (
    updateMetadata,
    deleteMetadata,
    getSingleMetadata,

    createMetadata,
    getMetadata,
    getMetaFamily, 
)

urlpatterns = [
    path('', getChildrenImages),
    
    path('list/', getListImages),

    path('latest/', getLatestImage),
    path('tags-latest/', getLatestTag),
    
    path('new-comments/', getNewComments),
    path('new/', getNewAlbum),

    path('tags/', getTagsList),
    path('all-tags/', getAllTags),
    path('tags-create/', createTag),

    path('posts/', getTagsPosts),

    path('upload/', uploadAlbumImage),
    path('upload-video/', uploadVideo),

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
    path('<str:pk>/public/', getIsPublicAlbum),

    path('images/<str:pk>/comments/', createImageComment),
    path('comments/<str:pk>/replies/', createCommentReply),
    path('comments/<str:pk>/', getComment),
    path('replies/<str:pk>/', getReply),
    path('comments/<str:pk>/update', updateComment),
    path('comments/<str:pk>/delete', deleteComment),
    path('replies/<str:pk>/update', updateReply),
    path('replies/<str:pk>/delete', deleteReply),

    path('albums/<str:pk>/album-likes/', createAlbumLike),
    path('albums/<str:pk>/comment-likes/', createCommentLike),
    path('albums/<str:pk>/reply-likes/', createReplyLike),

    path('email/<str:pk>/', email_send),
    path('line/<str:pk>/', line_send),

    path('pdf/<str:pk>/', pdfExport),
]