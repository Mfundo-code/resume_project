from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Prefetch
from .models import Category, Project
from .serializers import CategorySerializer, ProjectSerializer, ProjectListSerializer

class CategoryViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet for viewing categories.
    Public access - no authentication required.
    """
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    
    @action(detail=True, methods=['get'])
    def projects(self, request, pk=None):
        """Get all projects for a specific category"""
        category = self.get_object()
        projects = category.projects.all()
        serializer = ProjectListSerializer(projects, many=True, context={'request': request})
        return Response(serializer.data)

class ProjectViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet for viewing projects.
    Public access - no authentication required.
    """
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    
    def get_serializer_class(self):
        if self.action == 'list':
            return ProjectListSerializer
        return ProjectSerializer
    
    @action(detail=False, methods=['get'])
    def featured(self, request):
        """Get featured projects"""
        featured_projects = self.get_queryset().filter(featured=True)
        serializer = self.get_serializer(featured_projects, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def by_category(self, request):
        """Get all projects grouped by category"""
        categories = Category.objects.prefetch_related(
            Prefetch('projects', queryset=Project.objects.all())
        ).all()
        
        result = []
        for category in categories:
            category_data = CategorySerializer(category, context={'request': request}).data
            projects = category.projects.all()
            projects_data = ProjectListSerializer(projects, many=True, context={'request': request}).data
            category_data['projects'] = projects_data
            result.append(category_data)
        
        return Response(result)