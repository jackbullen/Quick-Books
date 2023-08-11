from django.contrib import admin
from .models import Book, Review

class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'created_at')
    # list_filter = ('author')
    search_fields = ('title', 'author', 'about')
    list_per_page = 20
    
admin.site.register(Book, BookAdmin)
admin.site.register(Review)