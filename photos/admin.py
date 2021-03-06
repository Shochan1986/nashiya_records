from django.contrib import admin
from photos.models import (
    Image, Comment, ContentImage, CommentLike, Video,
    AlbumLike, Tags, Metadata, Reply, ReplyLike,
)
from django.utils.safestring import mark_safe


def notify(modeladmin, request, queryset):
    for pic in queryset:
        try:
            pic.line_push(request)
            pic.email_push(request)   
        except:
            pic.email_push(request)     


class TagsAdmin(admin.ModelAdmin):
    model = Tags
    list_display = ('name', 'number', 'edit')
    search_fields = ('name', )
    list_editable = ('name', 'number',)
    list_display_links = ('edit', )
    list_per_page = 25

    def edit(self, obj):
        return "EDIT"

    edit.admin_order_field = '編集'
    edit.short_description = '編集'


class CommentInline(admin.TabularInline):
    model = Comment
    extra = 1


class ReplyInline(admin.TabularInline):
    model = Reply
    extra = 1


class ContentImageInline(admin.TabularInline):
    model = ContentImage
    extra = 1


class AlbumLikesInline(admin.TabularInline):
    model = AlbumLike
    extra = 1


class CommentLikesInline(admin.TabularInline):
    model = CommentLike
    extra = 1


class ReplyLikesInline(admin.TabularInline):
    model = ReplyLike
    extra = 1


class ImageAdmin(admin.ModelAdmin):
    model = Image
    inlines = [
        ContentImageInline,
        CommentInline,
        AlbumLikesInline,
    ]
    list_display = ('show_image', 'title', 'author', 'date', 'ct_is_public', 'cimg_is_public', 'special', 'comment',)
    search_fields = ('title', 'author', 'comment', 'content', 'content_rt', 'tags__name', 'comments__author', 'comments__text')
    list_editable = ('title', 'author', 'date', 'comment', 'ct_is_public', 'cimg_is_public', 'special')
    exclude = ('content_rt',)
    ordering = ('-date', '-created',)
    list_per_page = 25
    actions = [notify]
    
    def show_image(self, obj):
        if obj.image_one:
            return mark_safe('<img src="{}" style="width:100px; height:100px; object-fit:cover">'.format(obj.image_one.build_url(secure=True)))
        else: 
            return mark_safe('<img src="{}" style="width:100px; height:100px; object-fit:cover">'.format('https://images.pexels.com/photos/7245333/pexels-photo-7245333.jpeg?cs=srgb&dl=pexels-olga-lioncat-7245333.jpg&fm=jpg'))
    show_image.admin_order_field = 'サムネイル'
    show_image.short_description = 'サムネイル'


class CommentAdmin(admin.ModelAdmin):
    model = Comment
    list_display = ('image', 'author', 'text')
    search_fields = ('image__title', 'author', 'text')
    inlines = [
        ReplyInline,
        CommentLikesInline,
    ]


class ReplyAdmin(admin.ModelAdmin):
    model = Reply
    list_display = ('author', 'text')
    search_fields = ('author', 'text')
    inlines = [
        ReplyLikesInline,
    ]


class ContentImageAdmin(admin.ModelAdmin):
    model = ContentImage
    list_display = ('show_image', 'image')
    list_editable = ('image',)
    search_fields = ('image__title',)
    list_per_page = 25

    def show_image(self, obj):
        return mark_safe('<img src="{}" style="width:100px; height:100px; object-fit:cover">'.format(obj.content_image.build_url(secure=True)))
    show_image.admin_order_field = 'サムネイル'
    show_image.short_description = 'サムネイル'


class MetadataAdmin(admin.ModelAdmin):
    model = Metadata
    list_display = ('title', 'note',)
    search_fields = ('title', 'description', 'note', 'site_name')
    list_editable = ('note',)
    list_per_page = 30


class VideoAdmin(admin.ModelAdmin):
    model = Video
    list_display = ('url', 'title', 'thumbnail', 'public_id')
    search_fields = ('url', 'title', 'album__title')
    list_editable = ('title', 'thumbnail', 'public_id')
    list_per_page = 30


admin.site.register(Image, ImageAdmin)
admin.site.register(ContentImage, ContentImageAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Reply, ReplyAdmin)
admin.site.register(AlbumLike)
admin.site.register(CommentLike)
admin.site.register(ReplyLike)
admin.site.register(Tags, TagsAdmin)
admin.site.register(Metadata, MetadataAdmin)
# admin.site.register(Video, VideoAdmin)

notify.short_description = 'Line・Emailに転載する'
