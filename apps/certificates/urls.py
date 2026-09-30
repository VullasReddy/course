from django.urls import path
from .views import MyCertificatesAPIView, DownloadCertificatePDFView, VerifyCertificateAPIView

urlpatterns = [
    path('certificates', MyCertificatesAPIView.as_view(), name='api-certificates'),
    path('certificates/<str:certificate_id>/download', DownloadCertificatePDFView.as_view(), name='api-download-cert'),
    path('certificates/verify/<str:certificate_id>', VerifyCertificateAPIView.as_view(), name='api-verify'),
]
