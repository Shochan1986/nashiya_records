from django.contrib import admin
from farm.models import Article, Field, Images, Pears

class ArticleAdmin(admin.ModelAdmin):
    model = Article

admin.site.register(Article, ArticleAdmin)
admin.site.register(Field)
admin.site.register(Images)
admin.site.register(Pears)
