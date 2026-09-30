from rest_framework import serializers
from .models import Certificate
from apps.courses.serializers import CourseListSerializer

class CertificateSerializer(serializers.ModelSerializer):
    course = CourseListSerializer(read_only=True)
    user_name = serializers.CharField(source='user.full_name', read_only=True)

    class Meta:
        model = Certificate
        fields = ['id', 'certificate_id', 'user_name', 'course', 'issue_date']
