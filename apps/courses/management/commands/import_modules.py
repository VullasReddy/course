import os
import re
from pathlib import Path
from django.core.management.base import BaseCommand, CommandError
from django.conf import settings
from apps.courses.models import Course, Module

class Command(BaseCommand):
    help = 'Import PDF modules for a course from media/courses/python-full-stack/'

    def add_arguments(self, parser):
        parser.add_argument('course_name', type=str, help='Name or partial title of the Course')

    def handle(self, *args, **options):
        course_query = options['course_name']
        
        # 1. Match Course by title or slug
        course = Course.objects.filter(title__icontains=course_query).first()
        if not course:
            course = Course.objects.filter(slug__icontains=course_query).first()
            
        if not course:
            raise CommandError(f"Course matching '{course_query}' not found. Available courses: {[c.title for c in Course.objects.all()]}")

        # 2. Determine folder path under MEDIA_ROOT/courses/
        folder_candidates = [
            course.slug,
            course.slug.replace('-development', ''),
            course_query.lower().replace(' ', '-'),
            "python-full-stack",
        ]
        
        target_dir = None
        relative_folder = None
        for cand in folder_candidates:
            dir_path = Path(settings.MEDIA_ROOT) / 'courses' / cand
            if dir_path.exists() and dir_path.is_dir():
                target_dir = dir_path
                relative_folder = f"courses/{cand}"
                break
                
        if not target_dir:
            default_dir = Path(settings.MEDIA_ROOT) / 'courses' / 'python-full-stack'
            if default_dir.exists():
                target_dir = default_dir
                relative_folder = "courses/python-full-stack"
            else:
                raise CommandError(f"Directory not found for course. Looked in: {Path(settings.MEDIA_ROOT) / 'courses' / 'python-full-stack'}")

        self.stdout.write(self.style.SUCCESS(f"Importing modules for Course: '{course.title}' from '{target_dir}'"))

        # Regex to parse filenames like module-01-introduction.pdf or module-1-intro.pdf
        pdf_pattern = re.compile(r'^module[_-](\d+)[_-]?(.*)\.pdf$', re.IGNORECASE)

        imported_count = 0
        skipped_count = 0

        pdf_files = sorted(list(target_dir.glob("*.pdf")))
        if not pdf_files:
            self.stdout.write(self.style.WARNING(f"No PDF files found in '{target_dir}'"))
            return

        for pdf_path in pdf_files:
            filename = pdf_path.name
            match = pdf_pattern.match(filename)
            if not match:
                self.stdout.write(self.style.WARNING(f"Skipping file '{filename}' (does not match module-XX format)"))
                continue

            order_str, raw_title = match.groups()
            order = int(order_str)
            
            # Clean title
            if raw_title:
                clean_title = raw_title.replace('-', ' ').replace('_', ' ').strip().title()
            else:
                clean_title = f"Module {order}"

            relative_pdf_path = f"{relative_folder}/{filename}"

            # Check if Module already exists for this course by order or title
            existing_module = Module.objects.filter(course=course, order=order).first()
            if not existing_module:
                existing_module = Module.objects.filter(course=course, title__iexact=clean_title).first()

            if existing_module:
                # Update pdf_file if missing or different
                if not existing_module.pdf_file or existing_module.pdf_file.name != relative_pdf_path:
                    existing_module.pdf_file.name = relative_pdf_path
                    existing_module.save()
                    self.stdout.write(self.style.SUCCESS(f"Updated PDF for existing Module {order}: '{existing_module.title}'"))
                else:
                    self.stdout.write(f"Skipping Module {order}: '{existing_module.title}' (Already exists)")
                skipped_count += 1
                continue

            # Create new Module
            Module.objects.create(
                course=course,
                title=clean_title,
                order=order,
                description=f"Comprehensive study module {order} covering {clean_title}.",
                pdf_file=relative_pdf_path
            )
            imported_count += 1
            self.stdout.write(self.style.SUCCESS(f"Successfully created Module {order}: '{clean_title}'"))

        self.stdout.write(self.style.SUCCESS(f"Done! Created {imported_count} new modules, skipped {skipped_count} existing modules."))
