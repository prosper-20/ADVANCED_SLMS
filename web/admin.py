from django.contrib import admin
from .models import Post

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['title', 'author']
    list_filter = ['title']
    list_editable = ['author']
    raw_id_fields =['author']
    prepopulated_fields = {"slug": ("title",)}



