from django.contrib import admin
from .models import Subject, Course, Module, Enrollment, CourseMaterials, Broadcast


admin.site.register(Broadcast)

@admin.register(CourseMaterials)
class CourseMaterials(admin.ModelAdmin):
    list_display = ('course', 'title', 'file')


@admin.register(Enrollment)
class EnrollmentAdmin(admin.ModelAdmin):
    list_display = ['course', 'student']
    list_filter = ['course']

@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ['title', 'slug']
    prepopulated_fields = {'slug': ('title',)}


class ModuleInline(admin.StackedInline):
    model = Module

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ['title', 'subject', 'created']
    list_filter = ['created', 'subject']
    search_fields = ['title', 'overview']
    prepopulated_fields = {'slug': ('title',)}
    inlines = [ModuleInline]
