from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from apps.courses.models import Course, Category, Instructor
from apps.learning.models import Enrollment
from apps.certificates.models import Certificate

def home_view(request):
    categories = Category.objects.all()
    featured_courses = Course.objects.filter(status='published', is_featured=True)[:6]
    trending_courses = Course.objects.filter(status='published').order_by('-rating')[:6]
    return render(request, 'public/home.html', {
        'categories': categories,
        'featured_courses': featured_courses,
        'trending_courses': trending_courses
    })

def courses_view(request):
    categories = Category.objects.all()
    instructors = Instructor.objects.all()
    return render(request, 'public/courses.html', {
        'categories': categories,
        'instructors': instructors
    })

def course_detail_view(request, slug_or_id):
    if str(slug_or_id).isdigit():
        course = get_object_or_404(Course, id=int(slug_or_id))
    else:
        course = get_object_or_404(Course, slug=slug_or_id)

    is_enrolled = False
    if request.user.is_authenticated:
        is_enrolled = Enrollment.objects.filter(user=request.user, course=course).exists()

    return render(request, 'public/course_detail.html', {
        'course': course,
        'is_enrolled': is_enrolled
    })

def login_view(request):
    if request.user.is_authenticated:
        return redirect('/dashboard/')
    return render(request, 'public/login.html')

def register_view(request):
    if request.user.is_authenticated:
        return redirect('/dashboard/')
    return render(request, 'public/register.html')

def about_view(request):
    return render(request, 'public/about.html')

def contact_view(request):
    return render(request, 'public/contact.html')

def privacy_view(request):
    return render(request, 'public/privacy.html')

def terms_view(request):
    return render(request, 'public/terms.html')

@login_required
def user_dashboard_view(request):
    enrollments = Enrollment.objects.filter(user=request.user).order_by('-last_accessed_at')
    completed_count = enrollments.filter(is_completed=True).count()
    certificates = Certificate.objects.filter(user=request.user)
    return render(request, 'dashboard/user_dashboard.html', {
        'enrollments': enrollments[:4],
        'total_enrolled': enrollments.count(),
        'completed_count': completed_count,
        'certificates_count': certificates.count()
    })

@login_required
def my_courses_view(request):
    return render(request, 'dashboard/my_courses.html')

@login_required
def course_player_view(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    enrollment = get_object_or_404(Enrollment, user=request.user, course=course)
    return render(request, 'dashboard/player.html', {'course': course, 'enrollment': enrollment})

@login_required
def certificates_view(request):
    certificates = Certificate.objects.filter(user=request.user)
    return render(request, 'dashboard/certificates.html', {'certificates': certificates})

def verify_certificate_view(request, certificate_id):
    cert = Certificate.objects.filter(certificate_id=certificate_id).first()
    return render(request, 'dashboard/verify_certificate.html', {'certificate': cert, 'certificate_id': certificate_id})

@login_required
def admin_dashboard_view(request):
    return render(request, 'admin_portal/dashboard.html')
