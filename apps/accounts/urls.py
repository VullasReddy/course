from django.urls import path
from .views import RegisterAPIView, LoginAPIView, LogoutAPIView

urlpatterns = [
    path('auth/register', RegisterAPIView.as_view(), name='api-register'),
    path('auth/login', LoginAPIView.as_view(), name='api-login'),
    path('auth/logout', LogoutAPIView.as_view(), name='api-logout'),
]
