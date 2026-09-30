from rest_framework import serializers
from .models import Enrollment, LessonProgress
from apps.courses.serializers import CourseListSerializer, CourseDetailSerializer

class EnrollmentSerializer(serializers.ModelSerializer):
    course = CourseListSerializer(read_only=True)
    class Meta:
        model = Enrollment
        fields = ['id', 'course', 'enrolled_at', 'progress_percent', 'is_completed', 'completed_at', 'last_accessed_at']

class CoursePlayerSerializer(serializers.ModelSerializer):
    course = CourseDetailSerializer(read_only=True)
    completed_lesson_ids = serializers.SerializerMethodField()
    class Meta:
        model = Enrollment
        fields = ['id', 'course', 'progress_percent', 'is_completed', 'completed_at', 'completed_lesson_ids']

    def get_completed_lesson_ids(self, obj):
        return list(LessonProgress.objects.filter(enrollment=obj, completed=True).values_list('lesson_id', flat=True))
