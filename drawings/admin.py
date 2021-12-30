from django.contrib import admin
from drawings.models import Drawing
from django.utils.safestring import mark_safe


def notify(modeladmin, request, queryset):
    for post in queryset:
        post.line_push(request)


class DrawingAdmin(admin.ModelAdmin):
    model = Drawing
    list_display = ('show_image', 'title', 'date', 'comment',)
    search_fields = ('title', 'comment', )
    list_editable = ('title', 'date', 'comment',)
    actions = [notify]

    def save_model(self, request, obj, form, change):
        obj.from_admin_site = True 
        obj.save()
        super(DrawingAdmin, self).save_model(request, obj, form, change)
    
    def show_image(self, obj):
        return mark_safe('<img src="{}" style="width:100px;height:auto;">'.format(obj.url_one))
    show_image.admin_order_field = 'サムネイル'
    show_image.short_description = 'サムネイル'
    

admin.site.register(Drawing, DrawingAdmin)

notify.short_description = '通知を送信する'
