from django.contrib import admin
from .models  import Book


class BookAdmin(admin.ModelAdmin):
    list_display = ["title", "author", "published_date"]
    search_fields = ["title", "author"]
    prepopulated_fields = {"slug": ("title",)}


admin.site.register(Book, BookAdmin)
