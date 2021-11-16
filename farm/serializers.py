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
    class Meta:
        model = Article
        fields = '__all__'