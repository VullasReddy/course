import uuid
from django.db import models
from django.conf import settings
from apps.courses.models import Course
from apps.learning.models import Enrollment

def generate_cert_id():
    return f"SPRING-2026-{uuid.uuid4().hex[:8].upper()}"

class Certificate(models.Model):
    certificate_id = models.CharField(max_length=50, unique=True, default=generate_cert_id)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='certificates')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='certificates')
    enrollment = models.OneToOneField(Enrollment, on_delete=models.CASCADE, related_name='certificate')
    issue_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.certificate_id} - {self.user.full_name}"
