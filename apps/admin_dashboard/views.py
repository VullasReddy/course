from rest_framework import generics, permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from apps.accounts.models import User
from apps.courses.models import Course, Category
from apps.learning.models import Enrollment
from apps.certificates.models import Certificate

class AdminStatsAPIView(APIView):
    permission_classes = [permissions.IsAdminUser]

    def get(self, request):
        return Response({
            'metrics': {
                'total_users': User.objects.count(),
                'total_courses': Course.objects.count(),
                'total_enrollments': Enrollment.objects.count(),
                'certificates_issued': Certificate.objects.count()
            }
        })
