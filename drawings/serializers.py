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
        fields = ['id', 'title', 'description', 'created', 'image_one', 'image_two', 'comments']


class CommentSerializer(serializers.ModelSerializer):
    main_text = serializers.SerializerMethodField(read_only=True) 
    likes_count = serializers.SerializerMethodField(read_only=True) 
    likes = serializers.SerializerMethodField(read_only=True) 
    likes_users = serializers.SerializerMethodField(read_only=True) 

    def get_main_text(self, obj):  
        return urlize(linebreaks(obj.text))

    def get_likes_count(self, obj):  
        return obj.likes.count()

    def get_likes(self, obj):
        likes = obj.likes.all()
        serializer = CommentLikeSerializer(likes, many=True)
        return serializer.data

    def get_likes_users(self, obj):
        users = obj.likes.values_list('user', flat=True)
        return users

    class Meta:
        model = Comment
        fields = ['id', 'drawing', 'author', 'text', 'created', 'main_text', 'likes', 'likes_count', 'likes_users']


class CommentLikeSerializer(serializers.ModelSerializer):

    class Meta:
        model = CommentLike
        fields = ['id', 'user', 'created']