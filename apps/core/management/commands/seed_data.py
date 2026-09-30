from django.core.management.base import BaseCommand
from apps.accounts.models import User, UserProfile
from apps.courses.models import Category, Instructor, Course, Module, Lesson
from apps.learning.models import Enrollment, LessonProgress
from apps.certificates.models import Certificate
from django.utils import timezone

class Command(BaseCommand):
    help = 'Seeds exact 4 primary courses for Arshith Enterprise Platform'

    def handle(self, *args, **options):
        self.stdout.write("Seeding Arshith platform exact 4 courses...")

        # Clear existing courses/categories if resetting
        Course.objects.all().delete()
        Category.objects.all().delete()
        Instructor.objects.all().delete()

        admin, _ = User.objects.get_or_create(
            email='admin@arshith.com',
            defaults={'full_name': 'Arshith Admin', 'role': 'admin', 'is_staff': True, 'is_superuser': True}
        )
        admin.set_password('AdminPass123!')
        admin.save()

        student, _ = User.objects.get_or_create(
            email='student@arshith.com',
            defaults={'full_name': 'Alex Mercer', 'role': 'student'}
        )
        student.set_password('StudentPass123!')
        student.save()
        UserProfile.objects.get_or_create(user=student, defaults={'designation': 'Software Engineer'})

        # Categories
        cat_py = Category.objects.create(name='Python Development', icon='fa-code', description='Master Python full stack ecosystem.')
        cat_web = Category.objects.create(name='Web Development', icon='fa-laptop-code', description='Modern web development technologies.')
        cat_db = Category.objects.create(name='Databases & SQL', icon='fa-database', description='Enterprise database management systems and SQL query optimization.')
        cat_ai = Category.objects.create(name='AI & Data Science', icon='fa-brain', description='Artificial intelligence, machine learning, and data analytics.')

        # Instructors
        inst1 = Instructor.objects.create(name='Dr. Alan Turing', designation='Principal AI Scientist', bio='Specialist in AI, neural networks, and machine learning architectures.', experience_years=15)
        inst2 = Instructor.objects.create(name='Rajesh Kumar', designation='Senior Full-Stack Architect', bio='Expert in Python Django REST framework, Web development, and SQL databases.', experience_years=12)

        sample_video = "https://commondatastorage.googleapis.com/gtv-videos-bucket/sample/BigBuckBunny.mp4"

        # 4 Specific Courses Requested by User
        courses_data = [
            {
                'code': 'PY-FS-101',
                'title': 'Python Full Stack Development',
                'cat': cat_py,
                'inst': inst2,
                'diff': 'Intermediate',
                'hours': 24.0,
                'rating': 4.95,
                'short': 'Complete end-to-end Python Full Stack development covering Python core, Django, REST APIs, database integration, and modern frontend.',
                'thumb': 'https://images.unsplash.com/photo-1526374965328-7f61d4dc18c5?w=600&auto=format&fit=crop&q=60',
                'modules': [
                    ('Module 1: Python Core & OOP Fundamentals', [('1. Python Setup & Advanced Syntax', 20), ('2. Object-Oriented Programming & Classes', 30)]),
                    ('Module 2: Django Web Framework & ORM', [('1. Django Architecture & Models', 25), ('2. Views, Templates & Routing', 35)]),
                    ('Module 3: Django REST Framework APIs', [('1. Building RESTful Endpoints', 30), ('2. JWT Authentication & Permissions', 25)]),
                ]
            },
            {
                'code': 'WEB-101',
                'title': 'Web Development',
                'cat': cat_web,
                'inst': inst2,
                'diff': 'Beginner',
                'hours': 18.0,
                'rating': 4.88,
                'short': 'Master foundational and modern Web Development with HTML5, CSS3, JavaScript ES6+, responsive design layouts, and API integration.',
                'thumb': 'https://images.unsplash.com/photo-1555066931-4365d14bab8c?w=600&auto=format&fit=crop&q=60',
                'modules': [
                    ('Module 1: HTML5 & Semantic Web Structure', [('1. HTML5 Elements & Forms', 15), ('2. Accessibility & SEO Standards', 20)]),
                    ('Module 2: CSS3 Styling & Flexbox/Grid Layouts', [('1. CSS Responsive Styling', 25), ('2. Modern Flexbox & Grid Systems', 30)]),
                    ('Module 3: JavaScript ES6+ & DOM Logic', [('1. JS Fundamentals & Functions', 25), ('2. DOM Manipulation & Async Fetch', 30)]),
                ]
            },
            {
                'code': 'SQL-101',
                'title': 'DBMS with SQL',
                'cat': cat_db,
                'inst': inst2,
                'diff': 'Intermediate',
                'hours': 16.0,
                'rating': 4.91,
                'short': 'Comprehensive DBMS architecture and enterprise SQL masterclass covering relational schema design, complex joins, indexing, and query optimization.',
                'thumb': 'https://images.unsplash.com/photo-1544383835-bda2bc66a55d?w=600&auto=format&fit=crop&q=60',
                'modules': [
                    ('Module 1: Relational Database Architecture', [('1. Relational Models & ER Diagrams', 20), ('2. Data Types & Constraints', 25)]),
                    ('Module 2: Enterprise SQL Queries & Joins', [('1. SELECT, WHERE, & Filtering', 20), ('2. INNER JOIN, LEFT JOIN, & Aggregations', 30)]),
                    ('Module 3: Indexing, Transactions & Optimization', [('1. Indexing Strategies & Performance', 25), ('2. ACID Transactions & Locking', 25)]),
                ]
            },
            {
                'code': 'AI-DS-101',
                'title': 'AI with Data Science',
                'cat': cat_ai,
                'inst': inst1,
                'diff': 'Advanced',
                'hours': 28.0,
                'rating': 4.96,
                'short': 'Master Artificial Intelligence and Data Science pipeline engineering using Python, Pandas, NumPy, Machine Learning algorithms, and Neural Networks.',
                'thumb': 'https://images.unsplash.com/photo-1677442136019-21780ecad995?w=600&auto=format&fit=crop&q=60',
                'modules': [
                    ('Module 1: Data Science Foundations with Python', [('1. Pandas & Data Cleaning Pipelines', 25), ('2. Exploratory Data Analysis & Viz', 30)]),
                    ('Module 2: Machine Learning Algorithms', [('1. Supervised Learning & Regression', 35), ('2. Classification & Model Evaluation', 35)]),
                    ('Module 3: Artificial Intelligence & Neural Nets', [('1. Introduction to Deep Learning', 30), ('2. PyTorch & Neural Network Training', 40)]),
                ]
            }
        ]

        for cdata in courses_data:
            course = Course.objects.create(
                course_code=cdata['code'],
                title=cdata['title'],
                category=cdata['cat'],
                instructor=cdata['inst'],
                difficulty=cdata['diff'],
                duration_hours=cdata['hours'],
                rating=cdata['rating'],
                short_description=cdata['short'],
                description=f"{cdata['short']} Hands-on enterprise modules, real-world case studies, and complete project labs.",
                thumbnail_url=cdata['thumb'],
                is_featured=True,
                requirements='• Basic computer literacy\n• Dedication to complete all video lessons and practical coding exercises.',
                learning_objectives=f"• Master {cdata['title']} enterprise best practices.\n• Build production-ready projects.\n• Earn an official verified completion certificate.",
                status='published'
            )

            for m_idx, (m_title, lessons_list) in enumerate(cdata['modules'], start=1):
                mod = Module.objects.create(course=course, title=m_title, order=m_idx)
                for l_idx, (l_title, l_dur) in enumerate(lessons_list, start=1):
                    Lesson.objects.create(
                        module=mod,
                        title=l_title,
                        duration_minutes=l_dur,
                        video_url=sample_video,
                        order=l_idx,
                        is_free_preview=(m_idx == 1 and l_idx == 1),
                        is_published=True,
                        content_html=f"<h3>Lesson Overview: {l_title}</h3><p>Welcome to <strong>{l_title}</strong> in the {cdata['title']} course track.</p>"
                    )

        # Sample Enrollment for Demo Student on Python Full Stack
        py_course = Course.objects.get(course_code='PY-FS-101')
        enrollment, _ = Enrollment.objects.get_or_create(
            user=student,
            course=py_course,
            defaults={'progress_percent': 100.0, 'is_completed': True, 'completed_at': timezone.now()}
        )
        for les in Lesson.objects.filter(module__course=py_course):
            LessonProgress.objects.get_or_create(enrollment=enrollment, lesson=les, defaults={'completed': True, 'completed_at': timezone.now()})
        enrollment.update_progress()

        Certificate.objects.get_or_create(user=student, course=py_course, enrollment=enrollment)

        self.stdout.write(self.style.SUCCESS("Arshith 4 primary courses seeded successfully!"))

        # Seed Flagship SQL Mastery Course
        from django.core.management import call_command
        call_command('seed_sql_course')

        sql_mastery_course = Course.objects.filter(course_code='SQL-MASTERY').first()
        if sql_mastery_course:
            Enrollment.objects.get_or_create(user=student, course=sql_mastery_course)
