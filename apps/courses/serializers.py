from rest_framework import serializers
from .models import Category, Instructor, Course, Module, Lesson

class CategorySerializer(serializers.ModelSerializer):
    course_count = serializers.IntegerField(source='courses.count', read_only=True)
    class Meta:
        model = Category
        fields = ['id', 'name', 'slug', 'description', 'icon', 'course_count']

class InstructorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Instructor
        fields = ['id', 'name', 'designation', 'bio', 'experience_years']

class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = ['id', 'title', 'description', 'content_html', 'video_url', 'duration_minutes', 'order', 'is_free_preview']

class ModuleSerializer(serializers.ModelSerializer):
    lessons = LessonSerializer(many=True, read_only=True)
    class Meta:
        model = Module
        fields = ['id', 'title', 'description', 'order', 'pdf_file', 'lessons']

class CourseListSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source='category.name', read_only=True)
    instructor_name = serializers.CharField(source='instructor.name', read_only=True)
    class Meta:
        model = Course
        fields = ['id', 'title', 'course_code', 'slug', 'short_description', 'thumbnail_url', 'category', 'category_name', 'instructor', 'instructor_name', 'difficulty', 'duration_hours', 'rating', 'status', 'is_featured']

class CourseDetailSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    instructor = InstructorSerializer(read_only=True)
    modules = ModuleSerializer(many=True, read_only=True)
    class Meta:
        model = Course
        fields = ['id', 'title', 'course_code', 'slug', 'short_description', 'description', 'thumbnail_url', 'category', 'instructor', 'difficulty', 'duration_hours', 'rating', 'requirements', 'learning_objectives', 'status', 'modules']
