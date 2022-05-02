from rest_framework import serializers
from photos.models import Image, Comment
from django.utils.html import linebreaks, urlize
import cloudinary


class ChildrenImageSerializer(serializers.ModelSerializer):
    note = serializers.SerializerMethodField(read_only=True)
    image_one = serializers.SerializerMethodField(read_only=True)
    thumb_one = serializers.SerializerMethodField(read_only=True)
    image_two = serializers.SerializerMethodField(read_only=True)
    thumb_two = serializers.SerializerMethodField(read_only=True)
    ctIsPublic = serializers.SerializerMethodField(read_only=True)
    comments = serializers.SerializerMethodField(read_only=True)

    def get_note(self, obj):
        return obj.comment

    def get_image_one(self, obj):
        return obj.image_one.build_url(secure=True)

    def get_image_two(self, obj):
        if obj.image_two:
            return obj.image_two.build_url(secure=True)
        else:
            return None

    def get_thumb_one(self, obj):
        return obj.image_one.build_url(secure=True)

    def get_thumb_two(self, obj):
        if obj.image_two:
            return obj.image_two.build_url(secure=True)
        else:
            return None

    def get_ctIsPublic(self, obj):
        return obj.ct_is_public

    def get_comments(self, obj):
        comments = obj.comments.all()
        serializer = CommentSerializer(comments, many=True)
        return serializer.data

    def to_representation(self, instance):
        representation = super(ChildrenImageSerializer, self).to_representation(instance)
        if instance.image_one:
            thumbnailUrl = cloudinary.utils.cloudinary_url(
                instance.image_one.build_url(
                secure=True,
                transformation=[
                {'width': 750 },
                {'fetch_format': "auto"},
                {'quality': 'auto:eco'},
                {'dpr': 'auto'},
                {'effect': 'auto_contrast'},
                ]))
            representation['thumb_one'] = thumbnailUrl[0]
        if instance.image_two:
            thumbnailUrl = cloudinary.utils.cloudinary_url(
                instance.image_two.build_url(
                secure=True,
                transformation=[
                {'width': 750 },
                {'fetch_format': "auto"},
                {'quality': 'auto:eco'},
                {'dpr': 'auto'},
                {'effect': 'auto_contrast'},
                ]))
            representation['thumb_two'] = thumbnailUrl[0]
        return representation

    class Meta:
        model = Image
        fields = ['id', 'title', 'date', 'note', 'created', 'image_one', 'image_two', 'thumb_one', 'thumb_two', 'content', 'content_rt', 'ctIsPublic', 'special', 'comments']
    

class CommentSerializer(serializers.ModelSerializer):
    main_text = serializers.SerializerMethodField(read_only=True) 

    def get_main_text(self, obj):  
        return urlize(linebreaks(obj.text))

    class Meta:
        model = Comment
        fields = ['id', 'image', 'author', 'text', 'created', 'main_text']