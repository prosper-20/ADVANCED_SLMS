from django.contrib import admin
from .models import Post, Newsletter, Category


class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name']
    prepopulated_fields = {"slug": ("name",)}
admin.site.register(Category, CategoryAdmin)


admin.site.register(Newsletter)

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'category']
    list_filter = ['title']
    list_editable = ['author', 'category']
    raw_id_fields =['author']
    prepopulated_fields = {"slug": ("title",)}



