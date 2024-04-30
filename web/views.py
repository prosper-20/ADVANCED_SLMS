from django.shortcuts import render
from django.views import View
from courses.models import Course
from django.contrib import auth
from django.urls import reverse
from django.shortcuts import redirect
from django.contrib import messages
from django.contrib.auth import get_user_model

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
        return render(request, 'web/index.html', {"courses": courses})
    

class CoursesPage(View):
    def get(self, request):
        courses = Course.objects.all()
        return render(request, 'web/courses.html', {"courses": courses})
    
class CourseDetailPage(View):
    def get(self, request, slug):
        course = Course.objects.get(slug=slug)
        return render(request, 'web/course.html', {"course": course})

class AboutUsPage(View):
    def get(self, request):
        return render(request, 'web/about.html')

    

