from rest_framework import serializers
from farm.models import Article, Field, Pears, Images
from django.contrib.auth.models import User


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
        return ids
        
    def get_pears_names(self, obj):
        ids = obj.pears.values_list('name', flat=True)
        return ids

    class Meta:
        model = Article
        fields = ['id', 'title', 'field', 'task', 'description', 'start_time', 'end_time', 'created', 'updated', 'is_public', 
                'published_at', 'images', 'pears', 'pears_ids', 'pears_names']