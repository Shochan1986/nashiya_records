from rest_framework import serializers
from drawings.models import Drawing, Comment, CommentLike
from django.utils.html import linebreaks, urlize 
# import cloudinary


class DrawingSerializer(serializers.ModelSerializer):
    image_one = serializers.SerializerMethodField(read_only=True)
    image_two = serializers.SerializerMethodField(read_only=True)
    comments = serializers.SerializerMethodField(read_only=True)

    def get_image_one(self, obj):
        return obj.image_one.build_url(secure=True)

    def get_image_two(self, obj):
        if obj.image_two:
            return obj.image_two.build_url(secure=True)
        else:
            return None

    def get_comments(self, obj):
        comments = obj.comments.all()
        serializer = CommentSerializer(comments, many=True)
        return serializer.data

    class Meta:
        model = Drawing
        fields = ['id', 'title', 'date', 'description', 'created', 'image_one', 'image_two', 'comments']


class CommentSerializer(serializers.ModelSerializer):
    main_text = serializers.SerializerMethodField(read_only=True) 

    def get_main_text(self, obj):  
        return urlize(linebreaks(obj.text))

    class Meta:
        model = Comment
        fields = ['id', 'drawing', 'author', 'text', 'created', 'main_text',]