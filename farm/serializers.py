from rest_framework import serializers
from farm.models import Article, Fields, Pears, Images
from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import RefreshToken 
import cloudinary

class UserSerializer(serializers.ModelSerializer):
    _id = serializers.SerializerMethodField(read_only=True)
    isAdmin = serializers.SerializerMethodField(read_only=True)
    isSuper = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = User
        fields = ['id', '_id', 'first_name', 'username', 'email', 'isAdmin', 'isSuper']

    def get_isAdmin(self, obj):
        return obj.is_staff

    def get_isSuper(self, obj):
        return obj.is_superuser

    def get__id(self, obj):
        return obj.id


class UserSerializerWithToken(UserSerializer):
    token = serializers.SerializerMethodField(read_only=True)
    class Meta:
        model = User
        fields = ['id', '_id', 'first_name', 'username', 'email', 'isAdmin', 'isSuper', 'token', ]
    
    def get_token(self, obj):
        token = RefreshToken.for_user(obj)
        return str(token.access_token)


class FieldsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Fields
        fields = '__all__'


class PearsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pears
        fields = '__all__'


class ImagesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Images
        fields = '__all__'


class ArticleSerializer(serializers.ModelSerializer):
    pears = serializers.PrimaryKeyRelatedField(queryset=Pears.objects.all(), write_only=True)
    pears_ids = serializers.SerializerMethodField(read_only=True)
    pears_names = serializers.SerializerMethodField(read_only=True)
    fields = serializers.PrimaryKeyRelatedField(queryset=Fields.objects.all(), write_only=True)
    fields_ids = serializers.SerializerMethodField(read_only=True)
    fields_names = serializers.SerializerMethodField(read_only=True)
    images = serializers.PrimaryKeyRelatedField(queryset=Images.objects.all(), write_only=True)
    images_ids = serializers.SerializerMethodField(read_only=True)
    images_urls = serializers.SerializerMethodField(read_only=True)
    images_data = serializers.SerializerMethodField(read_only=True)

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

    def get_images_urls(self, obj):
        urls = obj.images.values_list('url', flat=True)
        return urls

    def get_images_data(self, obj):
        images = obj.images.all()
        serializer = ImagesSerializer(images, many=True)
        return serializer.data

    class Meta:
        model = Article
        fields = ['id', 'title', 'fields', 'date', 'description', 'start_time', 'end_time', 'created', 'updated', 'is_public', 
                'published_at', 'images', 'pears', 'pears_ids', 'pears_names', 'fields', 'fields_ids', 'fields_names', 'images_ids', 'images_urls', 'images_data']