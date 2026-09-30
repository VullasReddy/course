from rest_framework import status, permissions, generics
from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django.utils import timezone
from .models import Enrollment, LessonProgress, ModuleProgress, ExamQuestion, ModuleExamAttempt, ModuleExamAnswer
from .serializers import EnrollmentSerializer, CoursePlayerSerializer
from apps.courses.models import Course, Module, Lesson
from .openai_service import generate_lesson_content_openai

class EnrollCourseAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, course_id):
        course = get_object_or_404(Course, id=course_id)
        enrollment, created = Enrollment.objects.get_or_create(user=request.user, course=course)
        return Response({'message': 'Enrolled successfully', 'enrollment_id': enrollment.id})

class MyCoursesAPIView(generics.ListAPIView):
    serializer_class = EnrollmentSerializer
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = None

    def get_queryset(self):
        return Enrollment.objects.filter(user=self.request.user)

class CoursePlayerAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, course_id):
        enrollment = get_object_or_404(Enrollment, user=request.user, course_id=course_id)
        data = CoursePlayerSerializer(enrollment).data

        # Add per-module completion and exam metadata
        completed_lesson_ids = set(data.get('completed_lesson_ids', []))
        modules_metadata = []

        for mod in enrollment.course.modules.all():
            mod_lessons = mod.lessons.filter(is_published=True)
            total_mod_lessons = mod_lessons.count()
            completed_mod_lessons = sum(1 for les in mod_lessons if les.id in completed_lesson_ids)
            
            is_all_lessons_done = (total_mod_lessons > 0 and completed_mod_lessons == total_mod_lessons)
            
            mod_prog = ModuleProgress.objects.filter(enrollment=enrollment, module=mod).first()
            is_passed = mod_prog.completed if mod_prog else False
            best_score = float(mod_prog.best_score) if mod_prog else 0.0

            modules_metadata.append({
                'module_id': mod.id,
                'title': mod.title,
                'order': mod.order,
                'total_lessons': total_mod_lessons,
                'completed_lessons': completed_mod_lessons,
                'exam_unlocked': is_all_lessons_done,
                'exam_passed': is_passed,
                'best_score': best_score
            })

        data['modules_metadata'] = modules_metadata
        return Response(data)

class CompleteLessonAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, lesson_id):
        lesson = get_object_or_404(Lesson, id=lesson_id)
        enrollment = get_object_or_404(Enrollment, user=request.user, course=lesson.module.course)
        
        progress, _ = LessonProgress.objects.get_or_create(enrollment=enrollment, lesson=lesson)
        is_completed = request.data.get('completed', True)
        progress.completed = is_completed
        progress.completed_at = timezone.now() if is_completed else None
        progress.save()

        new_progress = enrollment.update_progress()
        
        # Check if all lessons in the module are now completed
        mod = lesson.module
        mod_lessons = mod.lessons.filter(is_published=True)
        all_completed = True
        for l in mod_lessons:
            if not LessonProgress.objects.filter(enrollment=enrollment, lesson=l, completed=True).exists():
                all_completed = False
                break

        return Response({
            'message': 'Lesson status updated',
            'progress_percent': new_progress,
            'module_id': mod.id,
            'module_exam_unlocked': all_completed
        })

class GenerateCourseContentAPIView(APIView):
    """
    OpenAI Backend Content Generation Service.
    Generates educational HTML content via OpenAI API securely from the backend.
    Saves content in database and falls back gracefully if OpenAI credentials are missing.
    """
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        lesson_id = request.data.get('lesson_id')
        if not lesson_id:
            return Response({'error': 'lesson_id is required'}, status=status.HTTP_400_BAD_REQUEST)

        lesson = get_object_or_404(Lesson, id=lesson_id)
        course_name = lesson.module.course.title
        module_name = lesson.module.title
        lesson_title = lesson.title
        difficulty = request.data.get('difficulty', 'beginner')
        db_type = request.data.get('database', 'PostgreSQL')

        generated_html = generate_lesson_content_openai(
            course_name=course_name,
            module_name=module_name,
            lesson_title=lesson_title,
            difficulty=difficulty,
            db_type=db_type
        )

        if generated_html:
            lesson.content_html = generated_html
            lesson.save()
            return Response({
                'message': 'Content generated and saved successfully',
                'source': 'openai',
                'content_html': generated_html
            })
        else:
            return Response({
                'message': 'OpenAI key not configured or API call failed. Using stored/seeded fallback content.',
                'source': 'fallback_database',
                'content_html': lesson.content_html
            })

class ModuleExamAPIView(APIView):
    """
    GET: Returns exam questions for a module.
    SECURITY GUARANTEE: NEVER includes correct_option in the response payload!
    Unlocked ONLY if all lessons in the module are completed.
    """
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, module_id):
        module = get_object_or_404(Module, id=module_id)
        enrollment = get_object_or_404(Enrollment, user=request.user, course=module.course)

        # Check if all lessons in module are completed
        mod_lessons = module.lessons.filter(is_published=True)
        for les in mod_lessons:
            if not LessonProgress.objects.filter(enrollment=enrollment, lesson=les, completed=True).exists():
                return Response({
                    'error': f'Complete all {mod_lessons.count()} lessons in {module.title} to unlock the Module Assessment.',
                    'unlocked': False
                }, status=status.HTTP_403_FORBIDDEN)

        questions = list(ExamQuestion.objects.filter(module=module))
        import random
        random.shuffle(questions)
        
        questions_payload = []
        for q in questions:
            questions_payload.append({
                'id': q.id,
                'order': q.order,
                'question_text': q.question_text,
                'option_a': q.option_a,
                'option_b': q.option_b,
                'option_c': q.option_c,
                'option_d': q.option_d,
                'difficulty': q.difficulty,
                'marks': q.marks
            })

        mod_prog = ModuleProgress.objects.filter(enrollment=enrollment, module=module).first()
        attempts = ModuleExamAttempt.objects.filter(user=request.user, module=module).order_by('-started_at')

        return Response({
            'unlocked': True,
            'module_id': module.id,
            'module_title': module.title,
            'total_questions': len(questions),
            'passing_percentage': 70.0,
            'time_limit_minutes': 15,
            'questions': questions_payload,
            'is_passed': mod_prog.completed if mod_prog else False,
            'best_score': float(mod_prog.best_score) if mod_prog else 0.0,
            'previous_attempts_count': attempts.count()
        })

class SubmitModuleExamAPIView(APIView):
    """
    POST: Evaluates submitted student answers securely on the backend server.
    Calculates score, creates ModuleExamAttempt, and updates ModuleProgress.
    """
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, module_id):
        module = get_object_or_404(Module, id=module_id)
        enrollment = get_object_or_404(Enrollment, user=request.user, course=module.course)

        user_answers = request.data.get('answers', {})  # Dict: { question_id: "A" }
        questions = ExamQuestion.objects.filter(module=module)
        
        total_questions = questions.count()
        if total_questions == 0:
            return Response({'error': 'No exam questions configured for this module.'}, status=status.HTTP_400_BAD_REQUEST)

        correct_count = 0
        wrong_count = 0
        unanswered_count = 0

        attempt = ModuleExamAttempt.objects.create(
            user=request.user,
            course=module.course,
            module=module,
            total_questions=total_questions,
            submitted_at=timezone.now()
        )

        for q in questions:
            q_id_str = str(q.id)
            selected = user_answers.get(q_id_str, '').upper()
            
            if not selected:
                unanswered_count += 1
                is_correct = False
            elif selected == q.correct_option.upper():
                correct_count += 1
                is_correct = True
            else:
                wrong_count += 1
                is_correct = False

            ModuleExamAnswer.objects.create(
                attempt=attempt,
                question=q,
                selected_option=selected if selected else None,
                is_correct=is_correct
            )

        percentage = round((correct_count / total_questions) * 100, 2)
        is_passed = percentage >= 70.0

        attempt.correct_answers = correct_count
        attempt.wrong_answers = wrong_count
        attempt.unanswered = unanswered_count
        attempt.percentage = percentage
        attempt.passed = is_passed
        attempt.save()

        # Update ModuleProgress
        mod_prog, _ = ModuleProgress.objects.get_or_create(enrollment=enrollment, module=module)
        if percentage > float(mod_prog.best_score):
            mod_prog.best_score = percentage

        if is_passed:
            mod_prog.completed = True
            if not mod_prog.completed_at:
                mod_prog.completed_at = timezone.now()
        mod_prog.save()

        # Check next module unlock
        next_module = Module.objects.filter(course=module.course, order=module.order + 1).first()

        return Response({
            'message': 'Exam submitted and evaluated successfully.',
            'attempt_id': attempt.id,
            'total_questions': total_questions,
            'correct_answers': correct_count,
            'wrong_answers': wrong_count,
            'unanswered': unanswered_count,
            'percentage': percentage,
            'passed': is_passed,
            'passing_percentage': 70.0,
            'best_score': float(mod_prog.best_score),
            'next_module_unlocked': is_passed and (next_module is not None),
            'next_module_id': next_module.id if next_module else None
        })
