from rest_framework import serializers
from drawings.models import Drawing
# from django.utils.html import linebreaks, urlize 
# import cloudinary


class DrawingSerializer(serializers.ModelSerializer):
    image_one = serializers.SerializerMethodField(read_only=True)
    image_two = serializers.SerializerMethodField(read_only=True)

    def get_image_one(self, obj):
        return obj.image_one.build_url(secure=True)

    def get_image_two(self, obj):
        if obj.image_two:
            return obj.image_two.build_url(secure=True)
        else:
            return None

    class Meta:
        model = Drawing
        fields = '__all__'