from django.contrib import admin
from drawings.models import Drawing, Comment
from django.utils.safestring import mark_safe


def notify(modeladmin, request, queryset):
    for pic in queryset:
        pic.line_push(request)


class CommentInline(admin.TabularInline):
    model = Comment
    extra = 1


class DrawingAdmin(admin.ModelAdmin):
    model = Drawing
    inlines = [
        CommentInline,
    ]
    list_display = ('show_image', 'title', 'date', 'creator', 'description',)
    search_fields = ('title', 'description', )
    list_editable = ('title', 'date', 'creator', 'description',)
    list_per_page = 20
    actions = [notify]
    
    def show_image(self, obj):
        return mark_safe('<img src="{}" style="width:100px;height:auto;">'.format(obj.image_one.url))
    show_image.admin_order_field = 'サムネイル'
    show_image.short_description = 'サムネイル'


class CommentAdmin(admin.ModelAdmin):
    model = Comment
    list_display = ('drawing', 'author', 'text')
    search_fields = ('drawing__title', 'author', 'text')

    
admin.site.register(Drawing, DrawingAdmin)
admin.site.register(Comment, CommentAdmin)

notify.short_description = 'LINEに転載する'
