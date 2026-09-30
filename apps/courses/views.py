from rest_framework import generics, permissions
from django.db.models import Q
from .models import Category, Instructor, Course
from .serializers import CategorySerializer, InstructorSerializer, CourseListSerializer, CourseDetailSerializer

class CategoryListView(generics.ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [permissions.AllowAny]
    pagination_class = None

class InstructorListView(generics.ListAPIView):
    queryset = Instructor.objects.all()
    serializer_class = InstructorSerializer
    permission_classes = [permissions.AllowAny]
    pagination_class = None

class CourseListView(generics.ListAPIView):
    serializer_class = CourseListSerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        queryset = Course.objects.filter(status='published')
        search = self.request.query_params.get('search')
        if search:
            queryset = queryset.filter(
                Q(title__icontains=search) | Q(short_description__icontains=search) | Q(course_code__icontains=search)
            )
        category = self.request.query_params.get('category')
        if category:
            queryset = queryset.filter(category__slug=category)
        return queryset

class CourseDetailView(generics.RetrieveAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseDetailSerializer
    permission_classes = [permissions.AllowAny]


import os
from django.http import FileResponse, Http404
from django.contrib.auth.decorators import login_required
from django.views.decorators.clickjacking import xframe_options_sameorigin
from django.shortcuts import get_object_or_404
from .models import Module

@login_required
@xframe_options_sameorigin
def view_module_pdf(request, module_id):
    module = get_object_or_404(Module, id=module_id)
    if not module.pdf_file or not os.path.exists(module.pdf_file.path):
        raise Http404("Module PDF file not found.")
    
    response = FileResponse(open(module.pdf_file.path, 'rb'), content_type='application/pdf')
    filename = os.path.basename(module.pdf_file.name)
    response['Content-Disposition'] = f'inline; filename="{filename}"'
    return response

@login_required
def download_module_pdf(request, module_id):
    module = get_object_or_404(Module, id=module_id)
    if not module.pdf_file or not os.path.exists(module.pdf_file.path):
        raise Http404("Module PDF file not found.")
        
    response = FileResponse(open(module.pdf_file.path, 'rb'), content_type='application/pdf')
    filename = os.path.basename(module.pdf_file.name)
    response['Content-Disposition'] = f'attachment; filename="{filename}"'
    return response

