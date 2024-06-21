from django.shortcuts import render
from django.views import View
from courses.models import Course
from django.contrib import auth
from django.urls import reverse
from django.shortcuts import redirect
from django.contrib import messages
from courses.models import Subject
from django.contrib.auth import get_user_model
from .models import Post, Newsletter

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
            return redirect(reverse('web-home'))
        else:
            messages.info(request, "Invalid username/password")
            return redirect(reverse('web-login'))

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
    

class CourseDetailPage(View):
    def get(self, request, slug):
        course = Course.objects.get(slug=slug)
        other_courses = Course.objects.exclude(slug=slug)
        return render(request, 'web/course.html', {"course": course, 'other_courses': other_courses})

class AboutUsPage(View):
    def get(self, request):
        return render(request, 'web/about.html')
    

class BlogPage(View):
    def get(self, request):
        posts = Post.objects.all()
        return render(request, "web/blog.html", {"posts": posts})
    


# class NewsletterView(View):
#     def post(self, request)

    

