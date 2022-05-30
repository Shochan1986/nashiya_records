from rest_framework import serializers
from photos.models import Image, Comment, AlbumLike, Tags, ContentImage
from django.utils.html import linebreaks, urlize
from drf_recaptcha.fields import ReCaptchaV3Field
import cloudinary


class TagsSerializer(serializers.ModelSerializer):
    images_count = serializers.SerializerMethodField(read_only=True)

    def get_images_count(self, obj):  
        return obj.images.count()

    class Meta:
        model = Tags
        fields = ['id', 'name', 'created', 'images_count']


class ContentImageSerializer(serializers.ModelSerializer):
    album_id = serializers.SerializerMethodField(read_only=True)
    album_title = serializers.SerializerMethodField(read_only=True)
    content_image = serializers.SerializerMethodField(read_only=True)
    thumbnail = serializers.SerializerMethodField(read_only=True)
    blur = serializers.SerializerMethodField(read_only=True)

    def get_album_id(self, obj):
        if obj.image:
            return obj.image.id
        else:
            return None

    def get_album_title(self, obj):
        if obj.image:
            return obj.image.title
        else:
            return None

    def get_content_image(self, obj):
        return obj.content_image.build_url(secure=True)

    def get_thumbnail(self, obj):
        return obj.content_image.build_url(secure=True)

    def get_blur(self, obj):
        return obj.content_image.build_url(secure=True)

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
        fields = ['id', 'image', 'content_image', 'thumbnail' ,'album_id', 'album_title', 'blur']


class AlbumLikeSerializer(serializers.ModelSerializer):

    class Meta:
        model = AlbumLike
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
    tags = serializers.SerializerMethodField(read_only=True)
    content_images = serializers.SerializerMethodField(read_only=True)
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

    def get_tags(self, obj):
        tags = obj.tags.all()
        serializer = TagsSerializer(tags, many=True)
        return serializer.data

    def get_content_images(self, obj):
        cImages = obj.content_images.all()
        serializer = ContentImageSerializer(cImages, many=True)
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
        fields = ['id', 'title', 'date', 'note', 'created', 'image_one', 'image_two', 
            'thumb_one', 'thumb_two', 'content', 'content_rt', 
            'ctIsPublic', 'cimg_is_public' ,'special', 'blur',
            'comments', 'comments_count', 'likes', 'likes_count', 
            'tags', 'content_images', 'recaptcha']

    def validate(self, attrs):
        attrs.pop("recaptcha")
        return attrs
    

class CommentSerializer(serializers.ModelSerializer):
    main_text = serializers.SerializerMethodField(read_only=True) 
    recaptcha = ReCaptchaV3Field(action="comment")

    def get_main_text(self, obj):  
        return urlize(linebreaks(obj.text))

    class Meta:
        model = Comment
        fields = ['id', 'image', 'author', 'text', 'created', 'main_text', 'recaptcha']

    def validate(self, attrs):
        attrs.pop("recaptcha")
        return attrs