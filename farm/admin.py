from django.contrib import admin
from farm.models import Article, Fields, Images, Pears

class ArticleAdmin(admin.ModelAdmin):
    model = Article

admin.site.register(Article, ArticleAdmin)
admin.site.register(Fields)
admin.site.register(Images)
admin.site.register(Pears)

admin.site.site_header = "梨屋さん 日報アプリ"
admin.site.index_title = '編集画面'                
admin.site.site_title = '梨屋さん 日報アプリ：管理サイト' 