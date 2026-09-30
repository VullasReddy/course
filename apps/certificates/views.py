from rest_framework import generics, permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from .models import Certificate
from .serializers import CertificateSerializer
from .pdf_generator import generate_certificate_pdf

class MyCertificatesAPIView(generics.ListAPIView):
    serializer_class = CertificateSerializer
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = None

    def get_queryset(self):
        return Certificate.objects.filter(user=self.request.user)

class DownloadCertificatePDFView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, certificate_id):
        cert = get_object_or_404(Certificate, certificate_id=certificate_id, user=request.user)
        pdf_bytes = generate_certificate_pdf(cert)
        response = HttpResponse(pdf_bytes, content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="Certificate-{cert.certificate_id}.pdf"'
        return response

class VerifyCertificateAPIView(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request, certificate_id):
        try:
            cert = Certificate.objects.get(certificate_id=certificate_id)
            return Response({
                'valid': True,
                'certificate_id': cert.certificate_id,
                'student_name': cert.user.full_name,
                'course_title': cert.course.title,
                'issue_date': cert.issue_date.strftime("%B %d, %Y")
            })
        except Certificate.DoesNotExist:
            return Response({'valid': False, 'error': 'Invalid Certificate ID'}, status=404)
