from django.contrib import admin
from .models import Project, ProjectScreenshot

class ProjectScreenshotInline(admin.TabularInline):
    model = ProjectScreenshot
    extra = 1
    readonly_fields = ('image_preview',)

    def image_preview(self, obj):
        if obj.image:
            from django.utils.html import mark_safe
            return mark_safe(f'<img src="{obj.image.url}" width="150" height="auto" />')
        return "No Image"
    image_preview.short_description = 'Image Preview'

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'technology')
    list_filter = ('category', 'tags', 'technology')
    search_fields = ('title', 'description', 'technology')
    inlines = [ProjectScreenshotInline]
    filter_horizontal = ('tags',)

@admin.register(ProjectScreenshot)
class ProjectScreenshotAdmin(admin.ModelAdmin):
    list_display = ('project', 'caption', 'image_preview')
    list_filter = ('project',)
    search_fields = ('caption',)
    readonly_fields = ('image_preview',)

    def image_preview(self, obj):
        if obj.image:
            from django.utils.html import mark_safe
            return mark_safe(f'<img src="{obj.image.url}" width="150" height="auto" />')
        return "No Image"
    image_preview.short_description = 'Image Preview'
