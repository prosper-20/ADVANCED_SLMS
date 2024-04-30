from django.urls import path
from .views import HomePage, CoursesPage, AboutUsPage, CourseDetailPage, LoginPage, SignUpPage

urlpatterns = [
    path("", HomePage.as_view(), name="web-home"),
    path("about/", AboutUsPage.as_view(), name="about-us"),
    path("courses/", CoursesPage.as_view(), name="courses"),
    path("courses/<slug:slug>/", CourseDetailPage.as_view(), name="course-detail"),
    path("login/", LoginPage.as_view(), name="web-login"),
    path("signup/", SignUpPage.as_view(), name="web-signup")
]