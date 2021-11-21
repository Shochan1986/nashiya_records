from rest_framework import serializers
from farm.models import Article, Field, Pears, Images
from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import RefreshToken 


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


class FieldSerializer(serializers.ModelSerializer):
    class Meta:
        model = Field
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

    def get_pears_ids(self, obj):
        ids = obj.pears.values_list('id', flat=True)
        if ids:
            dict = {(i + 1): True for i in range(0, len(ids))}
        else:
            dict = {(i + 1): False for i in range(0, len(ids))}
        return dict
        
    def get_pears_names(self, obj):
        ids = obj.pears.values_list('name', flat=True)
        return ids

    class Meta:
        model = Article
        fields = ['id', 'title', 'field', 'task', 'description', 'start_time', 'end_time', 'created', 'updated', 'is_public', 
                'published_at', 'images', 'pears', 'pears_ids', 'pears_names']