from tabnanny import verbose
from django.contrib import admin

from sales.models import ArticleCategory, Article, Sale

# Register your models here.
@admin.register(ArticleCategory)
class ArticleCategoryAdmin(admin.ModelAdmin):
    list_display = ("display_name",)
    list_filter = ("display_name",)

@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ("name", "code", "category","manufacturing_cost")
    list_filter = ("name", "category",)

@admin.register(Sale)
class SaleAdmin(admin.ModelAdmin):
    list_display = ("date", "author", "article", "quantity", "unit_selling_price",)
    list_filter = ("date", "author", "article")




