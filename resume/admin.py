from django.contrib import admin
from django.utils.html import format_html
from .models import Category, Project

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'created_at']
    list_filter = ['created_at']
    search_fields = ['name', 'description']

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = [
        'id', 
        'category', 
        'featured', 
        'created_at', 
        'project_image_preview',
        'tools_used_preview',
        'has_repo_link',
        'has_live_link'
    ]
    list_filter = ['category', 'featured', 'created_at']
    search_fields = ['description', 'tools_used']
    list_editable = ['featured']
    list_display_links = ['id', 'category']  # Make these clickable for editing
    
    # Add these fields to make editing easier
    fieldsets = (
        ('Basic Information', {
            'fields': ('category', 'featured', 'created_at', 'updated_at')
        }),
        ('Content', {
            'fields': ('description', 'project_image', 'project_image_preview')
        }),
        ('Technical Details', {
            'fields': ('tools_used', 'repo_link', 'live_link')
        }),
    )
    
    readonly_fields = ['created_at', 'updated_at', 'project_image_preview']
    
    # Custom methods for better display
    def project_image_preview(self, obj):
        if obj.project_image:
            return format_html(
                '<img src="{}" style="max-height: 100px; max-width: 100px;" />',
                obj.project_image.url
            )
        return "No image"
    project_image_preview.short_description = 'Image Preview'
    
    def tools_used_preview(self, obj):
        tools = obj.get_tools_list()
        if tools:
            return ', '.join(tools[:3]) + ('...' if len(tools) > 3 else '')
        return "No tools"
    tools_used_preview.short_description = 'Tools (Preview)'
    
    def has_repo_link(self, obj):
        return bool(obj.repo_link)
    has_repo_link.boolean = True
    has_repo_link.short_description = 'Repo Link'
    
    def has_live_link(self, obj):
        return bool(obj.live_link)
    has_live_link.boolean = True
    has_live_link.short_description = 'Live Link'