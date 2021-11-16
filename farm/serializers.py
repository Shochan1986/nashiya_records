from rest_framework import serializers
from farm.models import Article
from django.contrib.auth.models import User


class ArticleSerializerWithToken(serializers.ModelSerializer):
    class Meta:
        model = Article
        fields = '__all__'