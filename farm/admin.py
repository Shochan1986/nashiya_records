from django.contrib import admin
from farm.models import Article, Fields, Images, Pears, LinePush, Category, Comment
from django.utils.safestring import mark_safe

ADMIN_ORDERING = {
    "Farm" : [
        "Article",
        "Images",
        "Category",
        "Pears",
        "Fields",
        "Comment",
        "LinePush",
    ]
}

def get_app_list(self, request):
    app_dict = self._build_app_dict(request)
    for app_name, object_list in app_dict.items():
        if app_name in ADMIN_ORDERING:
            app = app_dict[app_name]
            app["models"].sort(
                key=lambda x: ADMIN_ORDERING[app_name].index(x["object_name"])
            )
            app_dict[app_name]
            yield app
        else:
            yield app_dict[app_name]


class CommentInline(admin.TabularInline):
    model = Comment
    extra = 1

class ArticleAdmin(admin.ModelAdmin):
    model = Article
    inlines = [
        CommentInline,
    ]
    list_display = ('title', 'date', 'user', 'category', 'is_public')
    list_editable = ('is_public', 'user', 'category')

    def save_model(self, request, obj, form, change):
        obj.from_admin_site = True 
        obj.save()
        super(ArticleAdmin, self).save_model(request, obj, form, change)


class ImagesAdmin(admin.ModelAdmin):
    model = Images
    list_display = ('show_image', 'comment', 'author', 'url',)
    list_editable = ('comment','author',)
    ordering = ('-created',)
    list_per_page = 15

    def show_image(self, obj):
        return mark_safe('<img src="{}" style="width:100px;height:auto;">'.format(obj.image.url))


class PearsAdmin(admin.ModelAdmin):
    model = Pears
    list_display = ('name', 'number')
    list_editable = ('number',)


class CategoryAdmin(admin.ModelAdmin):
    model = Category
    list_display = ('name', 'number')
    list_editable = ('number',)


class FieldsAdmin(admin.ModelAdmin):
    model = Fields
    list_display = ('name', 'number')
    list_editable = ('number',)


class LinePushAdmin(admin.ModelAdmin):
    model = LinePush
    list_display = ('line_name', 'unfollow', 'get_date_formatted', 'line_id', )
    list_editable = ('unfollow',)
    
    def change_view(self, request, object_id, form_url='', extra_context=None):
        self.readonly_fields = (
            'line_id',
            'line_status_message'
            )
        return self.changeform_view(request, object_id, form_url, extra_context)

    def add_view(self, request, form_url='', extra_context=None):
        self.readonly_fields = ()
        return self.changeform_view(request, None, form_url, extra_context)
    
    def get_date_formatted(self, obj):
        if obj:
            return obj.create_time.date()
    get_date_formatted.admin_order_field = '登録日'
    get_date_formatted.short_description = '登録日'


class CommentAdmin(admin.ModelAdmin):
    model = Comment
    list_display = ('article', 'author', 'text')

    def save_model(self, request, obj, form, change):
        obj.from_admin_site = True 
        obj.save()
        super(ArticleAdmin, self).save_model(request, obj, form, change)


admin.site.register(Article, ArticleAdmin)
admin.site.register(Fields, FieldsAdmin)
admin.site.register(Images, ImagesAdmin)
admin.site.register(Pears, PearsAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(LinePush, LinePushAdmin)
admin.site.register(Comment, CommentAdmin)

admin.AdminSite.get_app_list = get_app_list

admin.site.site_header = "梨屋さん 日報アプリ"
admin.site.index_title = '編集画面'                
admin.site.site_title = '梨屋さん 日報アプリ：管理サイト' 