from django.urls import path
from .views import AdminStatsAPIView

urlpatterns = [
    path('admin/stats', AdminStatsAPIView.as_view(), name='api-admin-stats'),
]
