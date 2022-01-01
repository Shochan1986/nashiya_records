from rest_framework import serializers
from photos.models import Image
# from django.utils.html import linebreaks, urlize 
# import cloudinary


class ChildrenImageSerializer(serializers.ModelSerializer):
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
        model = Image
        fields = '__all__'