from django.contrib import admin
from photos.models import Image
from django.utils.safestring import mark_safe


def notify(modeladmin, request, queryset):
    for pic in queryset:
        pic.line_push(request)


class ImageAdmin(admin.ModelAdmin):
    model = Image
    list_display = ('show_image', 'title', 'date', 'comment',)
    search_fields = ('title', 'comment', )
    list_editable = ('title', 'date', 'comment',)
    actions = [notify]

    def save_model(self, request, obj, form, change):
        obj.from_admin_site = True 
        obj.save()
        super(ImageAdmin, self).save_model(request, obj, form, change)
    
    def show_image(self, obj):
        return mark_safe('<img src="{}" style="width:100px;height:auto;">'.format(obj.image_one.build_url(secure=True)))
    show_image.admin_order_field = 'サムネイル'
    show_image.short_description = 'サムネイル'
    

admin.site.register(Image, ImageAdmin)

notify.short_description = 'LINEに転載する'
