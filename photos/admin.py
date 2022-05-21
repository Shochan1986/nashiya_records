from django.contrib import admin
from photos.models import Image, Comment, ContentImage, AlbumLike, Tags
from django.utils.safestring import mark_safe


def notify(modeladmin, request, queryset):
    for pic in queryset:
        pic.line_push(request)


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


class ContentImageInline(admin.TabularInline):
    model = ContentImage
    extra = 1

class AlbumLikesInline(admin.TabularInline):
    model = AlbumLike
    extra = 1


class ImageAdmin(admin.ModelAdmin):
    model = Image
    inlines = [
        CommentInline,
        ContentImageInline,
        AlbumLikesInline,
    ]
    list_display = ('show_image', 'title', 'date', 'ct_is_public', 'special', 'comment',)
    search_fields = ('title', 'comment', 'content', 'content_rt', 'tags__name')
    list_editable = ('title', 'date', 'comment', 'ct_is_public', 'special')
    exclude = ('content_rt',)
    list_per_page = 20
    actions = [notify]
    
    def show_image(self, obj):
        return mark_safe('<img src="{}" style="width:100px;height:auto;">'.format(obj.image_one.build_url(secure=True)))
    show_image.admin_order_field = 'サムネイル'
    show_image.short_description = 'サムネイル'


class CommentAdmin(admin.ModelAdmin):
    model = Comment
    list_display = ('image', 'author', 'text')
    search_fields = ('image__title', 'author', 'text')


admin.site.register(Image, ImageAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(AlbumLike)
admin.site.register(Tags, TagsAdmin)

notify.short_description = 'LINEに転載する'
