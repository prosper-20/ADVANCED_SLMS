from django.shortcuts import render, get_object_or_404
from django.views import View
from courses.models import Course, Enrollment
from django.contrib import auth
from django.urls import reverse
from django.shortcuts import redirect
from django.contrib import messages
from courses.models import Subject
from django.contrib.auth import get_user_model
from .models import Post, Newsletter, Category
from django.db.models import Count
from django.contrib.auth.mixins import LoginRequiredMixin
from courses.forms import BroadCastForm


User = get_user_model()

class StaffLoginPage(View):
    def get(self, request):
        return render(request, "web/authentication/staff_login.html")
    
    def post(self, request):
        email = request.POST['email']
        password = request.POST['password']

        user = auth.authenticate(email=email, password=password)

        if user is not None:
            auth.login(request, user)
            return redirect(reverse('web-staff-courses'))
        else:
            messages.info(request, "Invalid username/password")
            return redirect(reverse('web-login'))
        

def LecturerManageCoursePage(request):
    courses = Course.objects.filter(owner=request.user)
    return render(request, "web/lecturer_manage_course.html", {"courses": courses})

class LoginPage(View):
    def get(self, request):
        return render(request, "web/authentication/login.html")
    
    def post(self, request):
        email = request.POST['email']
        password = request.POST['password']

        user = auth.authenticate(email=email, password=password)

        if user is not None:
            auth.login(request, user)
            return redirect(reverse('web-home'))
        else:
            messages.info(request, "Invalid username/password")
            return redirect(reverse('web-login'))


class SignUpPage(View):
    def get(self, request):
        return render(request, "web/authentication/signup.html")
    
    def post(self, request):
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        password2 = request.POST['password2']

        if password == password2:
            if User.objects.filter(email=email).exists():
                messages.info(request, "Email already exists")
                return redirect(reverse('web-signup'))
            elif User.objects.filter(username=username).exists():
                messages.info(request, "Username already exists")
                return redirect(reverse('web-signup'))
            else:
                User.objects.create_user(username=username, email=email, password=password)
                messages.info(request, "Account creation successful")
                return redirect(reverse('web-login'))
        else:
            messages.info(request, "Passwords do not match")
            return redirect(reverse('web-signup'))
        
class StaffSignUpPage(View):
    def get(self, request):
        return render(request, "web/authentication/staff_signup.html")
    
    def post(self, request):
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        password2 = request.POST['password2']

        if password == password2:
            if User.objects.filter(email=email).exists():
                messages.info(request, "Email already exists")
                return redirect(reverse('web-signup'))
            elif User.objects.filter(username=username).exists():
                messages.info(request, "Username already exists")
                return redirect(reverse('web-signup'))
            else:
                User.objects.create_lecturer(username=username, email=email, password=password)
                messages.info(request, "Account creation successful")
                return redirect(reverse('web-login'))
        else:
            messages.info(request, "Passwords do not match")
            return redirect(reverse('web-signup'))

class LogoutPage(View):
    def get(self, request):
        auth.logout(request)
        return redirect(reverse('web-home'))

class HomePage(View):
    def get(self, request):
        courses = Course.objects.all()[:3]
        posts = Post.objects.all()
        return render(request, 'web/index.html', {"courses": courses, "posts": posts})
    
    def post(self, request):
        email = request.POST.get('email')
        if Newsletter.objects.filter(email=email).exists():
            messages.info(request, 'You are already subscribed to this newsletter')
        else:
            Newsletter.objects.create(email=email)
            messages.info(request, 'You have successfully subscribed to this newsletter')
        return redirect(reverse('web-home'))
    

class CoursesPage(View):
    def get(self, request):
        courses = Course.objects.all()
        subjects = Subject.objects.all()
        return render(request, 'web/courses.html', {"courses": courses, "subjects": subjects})
    
    def post(self, request):
        email = request.POST.get('email')
        Newsletter.objects.create(email=email)
        messages.info(request, "You have successfully subscribed to our newsletter")
        return redirect(reverse("courses"))
    

class CourseDetailPage(LoginRequiredMixin, View):
    def get(self, request, slug):
        course = Course.objects.get(slug=slug)
        other_courses = Course.objects.exclude(slug=slug)
        return render(request, 'web/course.html', {"course": course, 'other_courses': other_courses})
    
    def post(self, request, slug):
        user=request.user
        course = Course.objects.get(slug=slug)
        if Enrollment.objects.filter(course=course, student=request.user).exists():
            messages.info(request, "You have already enrolled in this course")
        else:
            Enrollment.objects.create(course=course, student=user)
            messages.success(request, "You have successfully enrolled for this course")
        return redirect(reverse('course-detail', kwargs={'slug': slug}))
        


class AboutUsPage(View):
    def get(self, request):
        return render(request, 'web/about.html')
    

class BlogPage(View):
    def get(self, request):
        posts = Post.objects.all()
        return render(request, "web/blog.html", {"posts": posts})
    

class BlogDetailPage(View):
    def get(self, request, post_slug):
        post = get_object_or_404(Post, slug=post_slug)
        other_posts = Post.objects.exclude(slug=post_slug)
        categories_with_counts = Category.objects.annotate(post_count=Count('post'))
        return render(request, "web/blog_single.html", {"post": post, "other_posts": other_posts, "categories_with_counts": categories_with_counts})
    



# class NewsletterView(View):
#     def post(self, request)

    

