from django.contrib import admin
from farm.models import Article, Fields, Images, Pears, LinePush

class ArticleAdmin(admin.ModelAdmin):
    model = Article
    list_display = ('title', 'date', 'is_public')


class LinePushAdmin(admin.ModelAdmin):
    model = LinePush
    list_display = ('line_name', 'unfollow', 'get_date_formatted', 'line_id', )
    
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


admin.site.register(Article, ArticleAdmin)
admin.site.register(Fields)
admin.site.register(Images)
admin.site.register(Pears)
admin.site.register(LinePush, LinePushAdmin)

admin.site.site_header = "梨屋さん 日報アプリ"
admin.site.index_title = '編集画面'                
admin.site.site_title = '梨屋さん 日報アプリ：管理サイト' 