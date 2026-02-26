from django.contrib import admin
from .models import Author, Book

@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ['name', 'birth_year', 'country']
    search_fields = ['name']
    list_filter = ['country']

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'publication_year', 'is_available']
    list_filter = ['is_available', 'publication_year', 'author']
    search_fields = ['title', 'author__name', 'isbn']
    date_hierarchy = 'created_at'