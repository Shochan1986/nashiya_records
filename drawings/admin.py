from django.contrib import admin
from drawings.models import Drawing, Comment, CommentLike
from django.utils.safestring import mark_safe


def notify(modeladmin, request, queryset):
    for pic in queryset:
        pic.line_push(request)


class DrawingAdmin(admin.ModelAdmin):
    model = Drawing
    list_display = ('show_image', 'title', 'date', 'description',)
    search_fields = ('title', 'description', )
    list_editable = ('title', 'date', 'description',)
    actions = [notify]

    def save_model(self, request, obj, form, change):
        obj.from_admin_site = True 
        obj.save()
        super(DrawingAdmin, self).save_model(request, obj, form, change)
    
    def show_image(self, obj):
        return mark_safe('<img src="{}" style="width:100px;height:auto;">'.format(obj.image_one.url))
    show_image.admin_order_field = 'サムネイル'
    show_image.short_description = 'サムネイル'


class CommentAdmin(admin.ModelAdmin):
    model = Comment
    list_display = ('drawing', 'author', 'text')

    def save_model(self, request, obj, form, change):
        obj.from_admin_site = True 
        obj.save()
        super(CommentAdmin, self).save_model(request, obj, form, change)


class CommentLikeAdmin(admin.ModelAdmin):
    model = CommentLike

    def save_model(self, request, obj, form, change):
        obj.from_admin_site = True 
        obj.save()
        super(CommentLikeAdmin, self).save_model(request, obj, form, change)
    

admin.site.register(Drawing, DrawingAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(CommentLike, CommentLikeAdmin)

notify.short_description = 'LINEに転載する'
