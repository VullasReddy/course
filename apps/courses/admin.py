from django.contrib import admin
from .models import Category, Instructor, Course, Module, Lesson

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}

@admin.register(Instructor)
class InstructorAdmin(admin.ModelAdmin):
    list_display = ('name', 'designation', 'experience_years')

class ModuleInline(admin.StackedInline):
    model = Module
    extra = 1
    fields = ('order', 'title', 'description', 'pdf_file')

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('course_code', 'title', 'category', 'instructor', 'difficulty', 'status')
    list_filter = ('category', 'difficulty', 'status')
    search_fields = ('title', 'course_code', 'description')
    prepopulated_fields = {'slug': ('title',)}
    inlines = [ModuleInline]

class LessonInline(admin.TabularInline):
    model = Lesson
    extra = 1

@admin.register(Module)
class ModuleAdmin(admin.ModelAdmin):
    list_display = ('order', 'title', 'course', 'has_pdf')
    list_filter = ('course',)
    search_fields = ('title', 'course__title', 'description')
    ordering = ('course', 'order')
    inlines = [LessonInline]

    def has_pdf(self, obj):
        return bool(obj.pdf_file)
    has_pdf.boolean = True
    has_pdf.short_description = 'PDF Material'

@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = ('order', 'title', 'module', 'duration_minutes', 'is_published')
    list_filter = ('module__course', 'is_published')
    search_fields = ('title', 'module__title')
    ordering = ('module', 'order')
