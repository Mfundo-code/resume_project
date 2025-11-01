from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Prefetch
from django.core.mail import send_mail
from django.conf import settings
from .models import Category, Project, Contact
from .serializers import CategorySerializer, ProjectSerializer, ProjectListSerializer, ContactSerializer

class CategoryViewSet(viewsets.ReadOnlyModelViewSet):
   
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

class ContactViewSet(viewsets.ModelViewSet):
  
    queryset = Contact.objects.all()
    serializer_class = ContactSerializer
    http_method_names = ['post']  # Only allow POST for contact submissions
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            # Save the contact message
            contact = serializer.save()
            
            # Send email notification ONLY to admin (you) - no client confirmation
            try:
                subject = f"New Portfolio Contact from {contact.name}"
                message = f"""
                You have received a new contact message
                from your portfolio website:
                
                Name: {contact.name}
                Email: {contact.email}
                Message: 
                {contact.message}
                
                Received at: {contact.created_at}
                
                ---
                Please respond to this person!
                """
                
                send_mail(
                    subject,
                    message,
                    settings.DEFAULT_FROM_EMAIL,
                    [settings.DEFAULT_FROM_EMAIL],  # Send to yourself
                    fail_silently=False,
                )
                
                
            except Exception as e:
                # Log the error but don't fail the request
                print(f"Email forwarding failed: {e}")
            
            return Response(
                {
                    'message': 'Message received successfully! I will get back to you soon.',
                    'data': serializer.data
                }, 
                status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)