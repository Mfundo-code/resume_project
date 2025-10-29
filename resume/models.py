from django.db import models
from django.urls import reverse

class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name_plural = "Categories"
        ordering = ['name']
    
    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse('admin:resume_category_change', args=[self.id])

class Project(models.Model):
    description = models.TextField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='projects')
    project_image = models.ImageField(upload_to='projects/')
    tools_used = models.TextField(help_text="Comma-separated list of tools/frameworks used")
    repo_link = models.URLField(blank=True, verbose_name="Repository Link")
    live_link = models.URLField(blank=True, verbose_name="Live Demo Link")
    featured = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Project {self.id} - {self.category.name} - {self.description[:50]}..."
    
    def get_tools_list(self):
        """Return tools as a list"""
        return [tool.strip() for tool in self.tools_used.split(',')]
    
    def get_absolute_url(self):
        return reverse('admin:resume_project_change', args=[self.id])