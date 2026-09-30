from django.urls import path
from .views import (
    home_view, courses_view, course_detail_view, login_view, register_view,
    about_view, contact_view, privacy_view, terms_view,
    user_dashboard_view, my_courses_view, course_player_view, certificates_view,
    verify_certificate_view, admin_dashboard_view
)
from apps.courses.views import view_module_pdf, download_module_pdf

urlpatterns = [
    path('', home_view, name='home'),
    path('courses/', courses_view, name='courses'),
    path('courses/<str:slug_or_id>/', course_detail_view, name='course-detail'),
    path('login/', login_view, name='login'),
    path('register/', register_view, name='register'),
    path('about/', about_view, name='about'),
    path('contact/', contact_view, name='contact'),
    path('privacy/', privacy_view, name='privacy'),
    path('terms/', terms_view, name='terms'),

    path('dashboard/', user_dashboard_view, name='dashboard'),
    path('my-courses/', my_courses_view, name='my-courses'),
    path('player/<int:course_id>/', course_player_view, name='player'),
    path('certificates/', certificates_view, name='certificates'),
    path('verify-certificate/<str:certificate_id>/', verify_certificate_view, name='verify-certificate'),

    path('admin-portal/', admin_dashboard_view, name='admin-dashboard'),

    path('modules/<int:module_id>/pdf/', view_module_pdf, name='view_module_pdf'),
    path('modules/<int:module_id>/pdf/download/', download_module_pdf, name='download_module_pdf'),
]
