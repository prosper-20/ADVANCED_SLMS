from django.shortcuts import render, get_object_or_404
from .serializers import StudentCourseListSerializer, SubjectSerializer, CourseListSerializer, UserRegistrationSerializer
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from django.db.models import Count
from courses.models import Subject
from django.contrib.auth.mixins import LoginRequiredMixin
from courses.models import Course
from django.core.cache import cache

class ApiStudentsCoursesListView(APIView, LoginRequiredMixin):
    ''' Returns all courses that a logged in user is currently enrolled in'''
    def get(self, request):
        current_user = 1
        all_student_courses = Course.objects.filter(students__in=[current_user])
        serializer = StudentCourseListSerializer(all_student_courses, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    


class ApiStudentsDetailView(APIView, LoginRequiredMixin):
    ''' Returns a single course that a logged in user is currently enrolled in'''
    def get(self, request, id, slug):
        current_user = request.user
        all_student_courses = Course.objects.filter(students__in=[current_user])
        for course in all_student_courses:
            if course.id == id and course.slug == slug:
                current_course = course
                serializer = StudentCourseListSerializer(current_course)
        return Response(serializer.data, status=status.HTTP_200_OK)
    

class ApiStudentCourseEnrollView(APIView, LoginRequiredMixin):
    ''' Allows a student to enroll for a course '''
    def post(self, request, id, slug):
        current_user = request.user
        print(current_user)
        current_course = get_object_or_404(Course, id=id, slug=slug)
        if current_user in current_course.students.all():
            return Response({"Message": "You are already enrolled in this course"}, status=status.HTTP_400_BAD_REQUEST)
        current_course.students.add(current_user)
        return Response({"Success": "You have successfully enrolled for the course"}, status=status.HTTP_201_CREATED)
    


class ApiCourseListView(APIView):
    '''List all available courses in the DB'''
    def get(self, request, subject=None):
        subjects = cache.get('all_subjects')
        if not subjects:
            subjects = Subject.objects.annotate(
                            total_courses=Count('courses'))
            cache.set('all_subjects', subjects)
        all_courses = Course.objects.annotate(
                        total_modules=Count('modules'))
        if subject:
            subject = get_object_or_404(Subject, slug=subject)
            key = f'subject_{subject.id}_courses'
            courses = cache.get(key)
            if not courses:
                courses = all_courses.filter(subject=subject)
                cache.set(key, courses)
        else:
            courses = cache.get('all_courses')
            if not courses:
                courses = all_courses
                cache.set('all_courses', courses)
        subject_serializer = SubjectSerializer(subjects, many=True)
        course_serializer = CourseListSerializer(all_courses, many=True)
        combined = subject_serializer.data + course_serializer.data
        return Response(combined, status=status.HTTP_200_OK)
    


class ApiUserRegistrationView(APIView):
    def post(self, request):
        user = UserRegistrationSerializer(data=request.data)
        user.is_valid(raise_exception=True)
        user.save()
        return Response({"Message": "User Registration Successful"}, status=status.HTTP_201_CREATED)
        




    


