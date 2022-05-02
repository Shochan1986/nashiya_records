from django.contrib import admin
from photos.models import Image, Comment, ContentImage
from django.utils.safestring import mark_safe


def notify(modeladmin, request, queryset):
    for pic in queryset:
        pic.line_push(request)


class CommentInline(admin.TabularInline):
    model = Comment
    extra = 1


class ContentImageInline(admin.TabularInline):
    model = ContentImage
    extra = 1


class ImageAdmin(admin.ModelAdmin):
    model = Image
    inlines = [
        CommentInline,
        ContentImageInline,
    ]
    list_display = ('show_image', 'title', 'date', 'ct_is_public', 'special', 'comment',)
    search_fields = ('title', 'comment', )
    list_editable = ('title', 'date', 'comment', 'ct_is_public', 'special')
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

notify.short_description = 'LINEに転載する'
