from rest_framework import serializers
from farm.models import (
    Article, 
    ArticleLike,
    Fields, 
    Pears, 
    Images, 
    Category, 
    Comment, 
    CommentLike
    )
from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import RefreshToken 
from django.utils.html import linebreaks, urlize 
from drf_recaptcha.fields import ReCaptchaV3Field
import cloudinary

class UserSerializer(serializers.ModelSerializer):
    isAdmin = serializers.SerializerMethodField(read_only=True)
    isSuper = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = User
        fields = ['id', 'first_name', 'username', 'email', 'isAdmin', 'isSuper', ]

    def get_isAdmin(self, obj):
        return obj.is_staff

    def get_isSuper(self, obj):
        return obj.is_superuser

    def get__id(self, obj):
        return obj.id


class UserSerializerWithToken(UserSerializer):
    token = serializers.SerializerMethodField(read_only=True)
    recaptcha = ReCaptchaV3Field(action="auth", required_score=0.6,)
    class Meta:
        model = User
        fields = ['id', 'first_name', 'username', 'email', 'isAdmin', 'isSuper', 'token', 'recaptcha' ]
    
    def get_token(self, obj):
        token = RefreshToken.for_user(obj)
        return str(token.access_token)
    
    def validate(self, attrs):
        attrs.pop("recaptcha")
        return attrs


class FieldsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Fields
        fields = '__all__'


class PearsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pears
        fields = '__all__'


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class ImagesSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField(read_only=True)
    thumbnail = serializers.SerializerMethodField(read_only=True)
    class Meta:
        model = Images
        fields = '__all__'

    def get_image(self, obj):
        return obj.image.url

    def get_thumbnail(self, obj):
        return obj.image.url

    def to_representation(self, instance):
        representation = super(ImagesSerializer, self).to_representation(instance)
        if instance.image:
            imagelUrl = cloudinary.utils.cloudinary_url(
                instance.image.build_url(
                secure=True))
            representation['image'] = imagelUrl[0]
        if instance.image:
            thumbnailUrl = cloudinary.utils.cloudinary_url(
                instance.image.build_url(
                secure=True,
                transformation=[
                {'width': 450 },
                {'fetch_format': "auto"},
                {'quality': 'auto:eco'},
                {'dpr': 'auto'},
                {'effect': 'auto_contrast'},
                ]))
            representation['thumbnail'] = thumbnailUrl[0]
        return representation


class CommentSerializer(serializers.ModelSerializer):
    main_text = serializers.SerializerMethodField(read_only=True) 
    likes = serializers.SerializerMethodField(read_only=True) 
    likes_data = serializers.SerializerMethodField(read_only=True) 
    likes_users = serializers.SerializerMethodField(read_only=True) 

    def get_main_text(self, obj):  
        return urlize(linebreaks(obj.text))

    def get_likes(self, obj):  
        return obj.likes.count()

    def get_likes_data(self, obj):
        likes = obj.likes.all()
        serializer = CommentLikeSerializer(likes, many=True)
        return serializer.data

    def get_likes_users(self, obj):
        users = obj.likes.values_list('user', flat=True)
        return users

    class Meta:
        model = Comment
        fields = ['id', 'article', 'author', 'text', 'created', 'main_text', 'likes', 'likes_users', 'likes_data']


class ArticleLikeSerializer(serializers.ModelSerializer):

    class Meta:
        model = ArticleLike
        fields = ['id', 'user', 'created']


class CommentLikeSerializer(serializers.ModelSerializer):

    class Meta:
        model = CommentLike
        fields = ['id', 'user', 'created']


class ArticleSerializer(serializers.ModelSerializer):
    main_text = serializers.SerializerMethodField(read_only=True)
    user__id = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), write_only=True)
    user_first_name = serializers.SerializerMethodField(read_only=True)
    category_id = serializers.PrimaryKeyRelatedField(queryset=Category.objects.all(), write_only=True)
    category_name = serializers.SerializerMethodField(read_only=True)
    pears = serializers.PrimaryKeyRelatedField(queryset=Pears.objects.all(), write_only=True)
    pears_ids = serializers.SerializerMethodField(read_only=True)
    pears_names = serializers.SerializerMethodField(read_only=True)
    fields = serializers.PrimaryKeyRelatedField(queryset=Fields.objects.all(), write_only=True)
    fields_ids = serializers.SerializerMethodField(read_only=True)
    fields_names = serializers.SerializerMethodField(read_only=True)
    images = serializers.PrimaryKeyRelatedField(queryset=Images.objects.all(), write_only=True)
    images_ids = serializers.SerializerMethodField(read_only=True)
    images_urls = serializers.SerializerMethodField(read_only=True)
    images_comments = serializers.SerializerMethodField(read_only=True)
    images_data = serializers.SerializerMethodField(read_only=True)
    comments = serializers.SerializerMethodField(read_only=True)
    likes_count = serializers.SerializerMethodField(read_only=True) 
    likes = serializers.SerializerMethodField(read_only=True) 

    def get_main_text(self, obj):  
        return urlize(linebreaks(obj.description))

    def get_pears_ids(self, obj):
        ids = obj.pears.values_list('id', flat=True)
        dict = {(ids[i]): True for i in range(0, len(ids))}
        return dict
        
    def get_pears_names(self, obj):
        names = obj.pears.values_list('name', flat=True)
        return names

    def get_fields_ids(self, obj):
        ids = obj.fields.values_list('id', flat=True)
        dict = {(ids[i]): True for i in range(0, len(ids))}
        return dict

    def get_fields_names(self, obj):
        names = obj.fields.values_list('name', flat=True)
        return names

    def get_images_ids(self, obj):
        ids = obj.images.values_list('id', flat=True)
        dict = {(ids[i]): True for i in range(0, len(ids))}
        return dict

    def get_images_comments(self, obj):
        ids = obj.images.values_list('comment', flat=True)
        dict = {(ids[i]): True for i in range(0, len(ids))}
        return dict

    def get_images_urls(self, obj):
        urls = obj.images.values_list('url', flat=True)
        return urls

    def get_images_data(self, obj):
        images = obj.images.all()
        serializer = ImagesSerializer(images, many=True)
        return serializer.data

    def get_category_id(self, obj):
        return obj.category.id

    def get_category_name(self, obj):
        if obj.category is not None:
            return obj.category.name
        else:
            return None

    def get_comments(self, obj):
        comments = obj.comments.all()
        serializer = CommentSerializer(comments, many=True)
        return serializer.data
    
    def get_user__id(self, obj):
        return obj.user.id

    def get_user_first_name(self, obj):
        if obj.user is not None:
            return obj.user.first_name
        else:
            return None

    def get_likes_count(self, obj):  
        return obj.likes.count()

    def get_likes(self, obj):
        likes = obj.likes.all()
        serializer = ArticleLikeSerializer(likes, many=True)
        return serializer.data

    class Meta:
        model = Article
        fields = ['id', 'user', 'title', 'category', 'category_id', 'category_name', 'fields', 'date', 'description', 'main_text', 
                'created', 'updated', 'is_public', 
                'published_at', 'images', 'pears', 'pears_ids', 'pears_names', 'fields', 'fields_ids', 'fields_names', 'images_ids', 
                'images_urls', 'images_comments', 'images_data', 'comments', 'user__id', 'user_first_name', 'likes', 'likes_count']
