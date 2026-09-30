from django.urls import path
from .views import CategoryListView, InstructorListView, CourseListView, CourseDetailView

urlpatterns = [
    path('categories', CategoryListView.as_view(), name='api-categories'),
    path('instructors', InstructorListView.as_view(), name='api-instructors'),
    path('courses', CourseListView.as_view(), name='api-courses'),
    path('courses/<int:pk>', CourseDetailView.as_view(), name='api-course-detail'),
]
