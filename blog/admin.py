from django.contrib import admin
from .models import BlogPost

@admin.register(BlogPost)
class BlogPostAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'category', 'published_date')
    list_filter = ('published_date', 'author', 'category', 'tags')
    search_fields = ('title', 'content')
    filter_horizontal = ('tags',)

