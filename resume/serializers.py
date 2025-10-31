from rest_framework import serializers
from .models import Category, Project, Contact

class CategorySerializer(serializers.ModelSerializer):
    project_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Category
        fields = ['id', 'name', 'description', 'project_count']
    
    def get_project_count(self, obj):
        return obj.projects.count()

class ProjectSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source='category.name', read_only=True)
    tools_list = serializers.SerializerMethodField()
    
    class Meta:
        model = Project
        fields = [
            'id', 'description', 'category', 'category_name', 
            'project_image', 'tools_used', 'tools_list', 'repo_link', 
            'live_link', 'featured', 'created_at', 'updated_at'
        ]
        read_only_fields = ['created_at', 'updated_at']
    
    def get_tools_list(self, obj):
        return obj.get_tools_list()

class ProjectListSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source='category.name', read_only=True)
    tools_list = serializers.SerializerMethodField()
    
    class Meta:
        model = Project
        fields = [
            'id', 'description', 'category_name', 'project_image', 
            'tools_list', 'repo_link', 'live_link', 'featured', 'created_at'
        ]
    
    def get_tools_list(self, obj):
        return obj.get_tools_list()

class ContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contact
        fields = ['id', 'name', 'email', 'message', 'created_at', 'is_read']
        read_only_fields = ['id', 'created_at', 'is_read']