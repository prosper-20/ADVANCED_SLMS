from django.urls import path
from .views import HomePage, CoursesPage, AboutUsPage, CourseDetailPage, BlogPage, LoginPage, SignUpPage, StaffLoginPage, StaffSignUpPage

urlpatterns = [
    path("", HomePage.as_view(), name="web-home"),
    path("blog/", BlogPage.as_view(), name="blog-page"),
    path("about/", AboutUsPage.as_view(), name="about-us"),
    path("courses/", CoursesPage.as_view(), name="courses"),
    path("courses/<slug:slug>/", CourseDetailPage.as_view(), name="course-detail"),
    path("login/", LoginPage.as_view(), name="web-login"),
    path("staff/login/", StaffLoginPage.as_view(), name="web-staff-login"),
    path("signup/", SignUpPage.as_view(), name="web-signup"),
    path("staff/signup/", StaffSignUpPage.as_view(), name="web-staff-signup")
]