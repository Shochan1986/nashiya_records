from rest_framework import serializers
from photos.models import (
    Image, Comment, AlbumLike, Tags, ReplyLike, Video,
    Reply, ContentImage, Metadata, CommentLike,
    )
from django.utils.html import linebreaks, urlize
from drf_recaptcha.fields import ReCaptchaV3Field
import cloudinary


class VideoSerializer(serializers.ModelSerializer):
    album_id = serializers.PrimaryKeyRelatedField(queryset=Image.objects.all(), write_only=True)
    album_title = serializers.SerializerMethodField(read_only=True)
    album_author = serializers.SerializerMethodField(read_only=True)
    album = serializers.SerializerMethodField(read_only=True)
    comment_bool = serializers.SerializerMethodField(read_only=True)
    reply_bool = serializers.SerializerMethodField(read_only=True)

    def get_album(self, obj):
        if obj.album:
            return obj.album.id
        else:
            return None

    def get_album_id(self, obj):
        if obj.album:
            return obj.album.id
        else:
            return None

    def get_album_title(self, obj):
        if obj.album:
            return obj.album.title
        else:
            return None

    def get_album_author(self, obj):
        if obj.album:
            return obj.album.author
        else:
            return None

    def get_comment_bool(self, obj):  
        if obj.comment:
            return True
        else:
            return False

    def get_reply_bool(self, obj):  
        if obj.reply:
            return True
        else:
            return False

    class Meta:
        model = Video
        fields = ['id', 'title', 'album_author', 'public_id', 'bytes',
            'url', 'author_id', 'author_name', 'thumbnail', 'comment_bool', 'reply_bool',
            'created', 'album', 'album_id', 'album_title', ]


class MetadataSerializer(serializers.ModelSerializer):
    album_id = serializers.PrimaryKeyRelatedField(queryset=Image.objects.all(), write_only=True)
    album_title = serializers.SerializerMethodField(read_only=True)
    album_author = serializers.SerializerMethodField(read_only=True)
    album = serializers.SerializerMethodField(read_only=True)
    comment_id = serializers.SerializerMethodField(read_only=True)
    reply_id = serializers.SerializerMethodField(read_only=True)
    comment_bool = serializers.SerializerMethodField(read_only=True)
    reply_bool = serializers.SerializerMethodField(read_only=True)

    def get_album(self, obj):
        if obj.album:
            return obj.album.id
        else:
            return None

    def get_album_id(self, obj):
        if obj.album:
            return obj.album.id
        else:
            return None

    def get_album_title(self, obj):
        if obj.album:
            return obj.album.title
        else:
            return None

    def get_album_author(self, obj):
        if obj.album:
            return obj.album.author
        else:
            return None

    def get_comment_id(self, obj):  
        if obj.comment:
            return obj.comment.id
        else:
            return None

    def get_reply_id(self, obj):  
        if obj.reply:
            return obj.reply.id
        else:
            return None

    def get_comment_bool(self, obj):  
        if obj.comment:
            return True
        else:
            return False

    def get_reply_bool(self, obj):  
        if obj.reply:
            return True
        else:
            return False

    class Meta:
        model = Metadata
        fields = ['id', 'site_url', 'title', 'image_url', 'note', 'family', 'album_author',
            'description', 'created', 'updated', 'site_name', 'comment_bool', 'reply_bool',
            'album', 'album_id', 'album_title', 'comment_id', 'reply_id', 'author']


class TagsSerializer(serializers.ModelSerializer):
    images_count = serializers.SerializerMethodField(read_only=True)

    def get_images_count(self, obj):  
        return obj.images.count()

    class Meta:
        model = Tags
        fields = ['id', 'name', 'created', 'images_count']


class ContentImageSerializer(serializers.ModelSerializer):
    album_id = serializers.PrimaryKeyRelatedField(queryset=Image.objects.all(), write_only=True)
    album_title = serializers.SerializerMethodField(read_only=True)
    album_author = serializers.SerializerMethodField(read_only=True)
    album = serializers.SerializerMethodField(read_only=True)
    cImage = serializers.SerializerMethodField(read_only=True)
    thumbnail = serializers.SerializerMethodField(read_only=True)
    blur = serializers.SerializerMethodField(read_only=True)
    main_text = serializers.SerializerMethodField(read_only=True)
    comment_bool = serializers.SerializerMethodField(read_only=True)
    reply_bool = serializers.SerializerMethodField(read_only=True)

    def get_album(self, obj):
        if obj.image:
            return obj.image.id
        else:
            return None

    def get_album_id(self, obj):
        if obj.image:
            return obj.image.id
        else:
            return None

    def get_album_author(self, obj):
        if obj.image:
            return obj.image.author
        else:
            return None

    def get_album_title(self, obj):
        if obj.image:
            return obj.image.title
        else:
            return None

    def get_cImage(self, obj):
        return obj.content_image.build_url(secure=True)

    def get_thumbnail(self, obj):
        return obj.content_image.build_url(secure=True)

    def get_blur(self, obj):
        return obj.content_image.build_url(secure=True)

    def get_main_text(self, obj):  
        if obj.note is not None:
            return urlize(linebreaks(obj.note))
        else:
            return None

    def get_comment_bool(self, obj):  
        if obj.comment:
            return True
        else:
            return False

    def get_reply_bool(self, obj):  
        if obj.reply:
            return True
        else:
            return False

    def to_representation(self, instance):
        representation = super(ContentImageSerializer, self).to_representation(instance)
        thumbnailUrl = cloudinary.utils.cloudinary_url(
            instance.content_image.build_url(
            secure=True,
            transformation=[
            {'width': 1250 },
            {'fetch_format': "auto"},
            {'quality': 'auto:best'},
            {'dpr': 'auto'},
            {'effect': 'auto_contrast'},
            ]))
        representation['cImage'] = thumbnailUrl[0]

    def to_representation(self, instance):
        representation = super(ContentImageSerializer, self).to_representation(instance)
        thumbnailUrl = cloudinary.utils.cloudinary_url(
            instance.content_image.build_url(
            secure=True,
            transformation=[
            {'width': 625 },
            {'fetch_format': "auto"},
            {'quality': 'auto:eco'},
            {'dpr': 'auto'},
            {'effect': 'auto_contrast'},
            ]))
        representation['thumbnail'] = thumbnailUrl[0]

    def to_representation(self, instance):
        representation = super(ContentImageSerializer, self).to_representation(instance)
        thumbnailUrl = cloudinary.utils.cloudinary_url(
            instance.content_image.build_url(
            secure=True,
            transformation=[
            {'width': 50},
            {'fetch_format': "auto"},
            {'quality': 'auto:eco'},
            {'dpr': 'auto'},
            ]))
        representation['blur'] = thumbnailUrl[0]
        return representation

    class Meta:
        model = ContentImage
        fields = ['id', 'image', 'cImage', 'note', 'created', 'updated', 
            'comment_bool', 'reply_bool', 'author',
            'thumbnail' ,'album', 'album_id', 'album_title', 'blur', 
            'main_text', 'album_author']


class AlbumLikeSerializer(serializers.ModelSerializer):

    class Meta:
        model = AlbumLike
        fields = ['id', 'user', 'created']


class CommentLikeSerializer(serializers.ModelSerializer):

    class Meta:
        model = CommentLike
        fields = ['id', 'user', 'created']


class ReplyLikeSerializer(serializers.ModelSerializer):

    class Meta:
        model = ReplyLike
        fields = ['id', 'user', 'created']


class ChildrenImageSerializer(serializers.ModelSerializer):
    note = serializers.SerializerMethodField(read_only=True)
    image_one = serializers.SerializerMethodField(read_only=True)
    thumb_one = serializers.SerializerMethodField(read_only=True)
    blur = serializers.SerializerMethodField(read_only=True)
    image_two = serializers.SerializerMethodField(read_only=True)
    thumb_two = serializers.SerializerMethodField(read_only=True)
    ctIsPublic = serializers.SerializerMethodField(read_only=True)
    comments = serializers.SerializerMethodField(read_only=True)
    comments_count = serializers.SerializerMethodField(read_only=True)
    likes_count = serializers.SerializerMethodField(read_only=True) 
    likes = serializers.SerializerMethodField(read_only=True)
    tags = serializers.PrimaryKeyRelatedField(queryset=Tags.objects.all(), write_only=True)
    tags_ids = serializers.SerializerMethodField(read_only=True)
    tags_data = serializers.SerializerMethodField(read_only=True)
    content_images = serializers.SerializerMethodField(read_only=True)
    metadata = serializers.SerializerMethodField(read_only=True)
    videos = serializers.SerializerMethodField(read_only=True)
    recaptcha = ReCaptchaV3Field(action="children-images")

    def get_note(self, obj):
        return obj.comment

    def get_image_one(self, obj):
        if obj.image_one:
            return obj.image_one.build_url(secure=True)
        else:
            None

    def get_image_two(self, obj):
        if obj.image_two:
            return obj.image_two.build_url(secure=True)
        else:
            return None

    def get_thumb_one(self, obj):
        if obj.image_one:
            return obj.image_one.build_url(secure=True)
        else:
            return None

    def get_blur(self, obj):
        if obj.image_one:
            return obj.image_one.build_url(secure=True)
        else:
            None

    def get_thumb_two(self, obj):
        if obj.image_two:
            return obj.image_two.build_url(secure=True)
        else:
            return None

    def get_ctIsPublic(self, obj):
        return obj.ct_is_public

    def get_comments(self, obj):
        comments = obj.comments.all()
        serializer = CommentSerializer(comments, many=True)
        return serializer.data

    def get_comments_count(self, obj):  
        return obj.comments.count()

    def get_likes_count(self, obj):  
        return obj.likes.count()

    def get_likes(self, obj):
        likes = obj.likes.all()
        serializer = AlbumLikeSerializer(likes, many=True)
        return serializer.data

    def get_tags_ids(self, obj):
        ids = obj.tags.values_list('id', flat=True)
        dict = {(ids[i]): True for i in range(0, len(ids))}
        return dict

    def get_tags_data(self, obj):
        tags = obj.tags.all()
        serializer = TagsSerializer(tags, many=True)
        return serializer.data

    def get_content_images(self, obj):
        cImages = obj.content_images.all()
        serializer = ContentImageSerializer(cImages, many=True)
        return serializer.data

    def get_metadata(self, obj):
        meta = obj.metadata.all()
        serializer = MetadataSerializer(meta, many=True)
        return serializer.data

    def get_videos(self, obj):
        video = obj.videos.all()
        serializer = VideoSerializer(video, many=True)
        return serializer.data

    def to_representation(self, instance):
        representation = super(ChildrenImageSerializer, self).to_representation(instance)
        if instance.image_one:
            thumbnailUrl = cloudinary.utils.cloudinary_url(
                instance.image_one.build_url(
                secure=True,
                transformation=[
                {'width': 625 },
                {'fetch_format': "auto"},
                {'quality': 'auto:eco'},
                {'dpr': 'auto'},
                {'effect': 'auto_contrast'},
                ]))
            representation['thumb_one'] = thumbnailUrl[0]
        if instance.image_one:
            thumbnailUrl = cloudinary.utils.cloudinary_url(
                instance.image_one.build_url(
                secure=True,
                transformation=[
                {'width': 50 },
                {'fetch_format': "auto"},
                {'quality': 'auto:eco'},
                {'dpr': 'auto'},
                ]))
            representation['blur'] = thumbnailUrl[0]
        if instance.image_two:
            thumbnailUrl = cloudinary.utils.cloudinary_url(
                instance.image_two.build_url(
                secure=True,
                transformation=[
                {'width': 625 },
                {'fetch_format': "auto"},
                {'quality': 'auto:eco'},
                {'dpr': 'auto'},
                {'effect': 'auto_contrast'},
                ]))
            representation['thumb_two'] = thumbnailUrl[0]
        return representation

    class Meta:
        model = Image
        fields = ['id', 'title', 'date', 'note', 'created', 'draft', 'author',
            'image_one', 'image_two', 'tags', 'tags_data', 'tags_ids', 
            'thumb_one', 'thumb_two', 'content', 'content_rt', 
            'ctIsPublic', 'cimg_is_public' ,'special', 'blur',
            'comments', 'comments_count', 'likes', 'likes_count', 'videos',
            'content_images', 'metadata', 'recaptcha']

    def validate(self, attrs):
        attrs.pop("recaptcha")
        return attrs


class ReplySerializer(serializers.ModelSerializer):
    main_text = serializers.SerializerMethodField(read_only=True) 
    content_images = serializers.SerializerMethodField(read_only=True)
    likes_count = serializers.SerializerMethodField(read_only=True) 
    likes = serializers.SerializerMethodField(read_only=True) 
    metadata = serializers.SerializerMethodField(read_only=True) 
    recaptcha = ReCaptchaV3Field(action="reply")

    def get_main_text(self, obj):  
        return urlize(linebreaks(obj.text))

    def get_content_images(self, obj):
        cImages = obj.content_images.all()
        serializer = ContentImageSerializer(cImages, many=True)
        return serializer.data

    def get_likes_count(self, obj):  
        return obj.likes.count()

    def get_likes(self, obj):
        likes = obj.likes.all()
        serializer = ReplyLikeSerializer(likes, many=True)
        return serializer.data
    
    def get_metadata(self, obj):
        meta = obj.metadata.all()
        serializer = MetadataSerializer(meta, many=True)
        return serializer.data

    class Meta:
        model = Reply
        fields = ['id', 'comment', 'author', 'content_images', 'likes_count', 
        'likes', 'text', 'created', 'main_text', 'recaptcha', 'metadata']

    def validate(self, attrs):
        attrs.pop("recaptcha")
        return
    

class CommentSerializer(serializers.ModelSerializer):
    main_text = serializers.SerializerMethodField(read_only=True)
    replies = serializers.SerializerMethodField(read_only=True) 
    content_images = serializers.SerializerMethodField(read_only=True) 
    likes_count = serializers.SerializerMethodField(read_only=True) 
    likes = serializers.SerializerMethodField(read_only=True) 
    metadata = serializers.SerializerMethodField(read_only=True) 
    recaptcha = ReCaptchaV3Field(action="comment")

    def get_main_text(self, obj):  
        return urlize(linebreaks(obj.text))

    def get_replies(self, obj):
        replies = obj.replies.all()
        serializer = ReplySerializer(replies, many=True)
        return serializer.data

    def get_content_images(self, obj):
        cImages = obj.content_images.all()
        serializer = ContentImageSerializer(cImages, many=True)
        return serializer.data

    def get_likes_count(self, obj):  
        return obj.likes.count()

    def get_likes(self, obj):
        likes = obj.likes.all()
        serializer = CommentLikeSerializer(likes, many=True)
        return serializer.data

    def get_metadata(self, obj):
        meta = obj.metadata.all()
        serializer = MetadataSerializer(meta, many=True)
        return serializer.data

    class Meta:
        model = Comment
        fields = ['id', 'image', 'author', 'replies', 'content_images', 'metadata',
            'text', 'created', 'main_text', 'likes_count', 'likes', 'recaptcha']

    def validate(self, attrs):
        attrs.pop("recaptcha")
        return  
        

class ImageTitleSerializer(serializers.ModelSerializer):

    class Meta:
        model = Image
        fields = ['id', 'title', 'author']


class AlbumSerializer(serializers.ModelSerializer):
    thumb_one = serializers.SerializerMethodField(read_only=True)
    blur = serializers.SerializerMethodField(read_only=True)
    ctIsPublic = serializers.SerializerMethodField(read_only=True)
    comments_count = serializers.SerializerMethodField(read_only=True)
    likes_count = serializers.SerializerMethodField(read_only=True) 
    content_count = serializers.SerializerMethodField(read_only=True) 
    meta_count = serializers.SerializerMethodField(read_only=True) 
    video_count = serializers.SerializerMethodField(read_only=True) 
    tags_data = serializers.SerializerMethodField(read_only=True)

    def get_thumb_one(self, obj):
        if obj.image_one:
            return obj.image_one.build_url(secure=True)
        else:
            return None

    def get_blur(self, obj):
        if obj.image_one:
            return obj.image_one.build_url(secure=True)
        else:
            None

    def get_ctIsPublic(self, obj):
        return obj.ct_is_public

    def get_comments_count(self, obj):  
        return obj.comments.count()

    def get_likes_count(self, obj):  
        return obj.likes.count()

    def get_tags_data(self, obj):
        tags = obj.tags.all()
        serializer = TagsSerializer(tags, many=True)
        return serializer.data
    
    def get_content_count(self, obj):
        return obj.content_images.filter(comment=None, reply=None).count()
    
    def get_meta_count(self, obj):
        return obj.metadata.filter(comment=None, reply=None).count()
    
    def get_video_count(self, obj):
        return obj.videos.all().count()

    def to_representation(self, instance):
        representation = super(AlbumSerializer, self).to_representation(instance)
        if instance.image_one:
            thumbnailUrl = cloudinary.utils.cloudinary_url(
                instance.image_one.build_url(
                secure=True,
                transformation=[
                {'width': 625 },
                {'fetch_format': "auto"},
                {'quality': 'auto:eco'},
                {'dpr': 'auto'},
                {'effect': 'auto_contrast'},
                ]))
            representation['thumb_one'] = thumbnailUrl[0]
        if instance.image_one:
            thumbnailUrl = cloudinary.utils.cloudinary_url(
                instance.image_one.build_url(
                secure=True,
                transformation=[
                {'width': 50 },
                {'fetch_format': "auto"},
                {'quality': 'auto:eco'},
                {'dpr': 'auto'},
                ]))
            representation['blur'] = thumbnailUrl[0]
        return representation

    class Meta:
        model = Image
        fields = ['id', 'title', 'date', 'created', 'draft', 'author',
            'tags_data', 'thumb_one', 'ctIsPublic', 'cimg_is_public' ,
            'special', 'blur', 'content', 'content_rt', 'video_count',
            'comments_count', 'likes_count', 'content_count', 'meta_count']

