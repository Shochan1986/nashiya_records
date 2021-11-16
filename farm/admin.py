from django.contrib import admin
from farm.models import Article

class ArticleAdmin(admin.ModelAdmin):
    model = Article

admin.site.register(Article, ArticleAdmin)
