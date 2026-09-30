from django.urls import path
from .views import (
    EnrollCourseAPIView, MyCoursesAPIView, CoursePlayerAPIView, CompleteLessonAPIView,
    GenerateCourseContentAPIView, ModuleExamAPIView, SubmitModuleExamAPIView
)

urlpatterns = [
    path('courses/<int:course_id>/enroll', EnrollCourseAPIView.as_view(), name='api-enroll'),
    path('my-courses', MyCoursesAPIView.as_view(), name='api-my-courses'),
    path('player/<int:course_id>', CoursePlayerAPIView.as_view(), name='api-player'),
    path('lessons/<int:lesson_id>/complete', CompleteLessonAPIView.as_view(), name='api-complete'),
    path('course-content/generate', GenerateCourseContentAPIView.as_view(), name='api-generate-content'),
    path('modules/<int:module_id>/exam', ModuleExamAPIView.as_view(), name='api-module-exam'),
    path('modules/<int:module_id>/exam/submit', SubmitModuleExamAPIView.as_view(), name='api-submit-module-exam'),
]
