from rest_framework import serializers
from photos.models import Image
# from django.utils.html import linebreaks, urlize 
# import cloudinary


class ChildrenImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = '__all__'