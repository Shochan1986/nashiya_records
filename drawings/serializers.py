from rest_framework import serializers
from drawings.models import Drawing
# from django.utils.html import linebreaks, urlize 
# import cloudinary


class DrawingSerializer(serializers.ModelSerializer):

    class Meta:
        model = Drawing
        fields = '__all__'