from django.urls import path
from .views import HomePage, CoursesPage, AboutUsPage, CourseDetailPage, BlogPage, BlogDetailPage, LoginPage,SignUpPage, StaffLoginPage, StaffSignUpPage
from courses.views import BroadCastView


urlpatterns = [
    path("", HomePage.as_view(), name="web-home"),
    path("blog/", BlogPage.as_view(), name="blog-page"),
    path("blog/<slug:post_slug>/", BlogDetailPage.as_view(), name="blog-detail"),
    path("about/", AboutUsPage.as_view(), name="about-us"),
    path("courses/", CoursesPage.as_view(), name="courses"),
    path("courses/broadcast/", BroadCastView.as_view(), name="broadcast"),
    path("courses/<slug:slug>/", CourseDetailPage.as_view(), name="course-detail"),
    path("login/", LoginPage.as_view(), name="web-login"),
    path("staff/login/", StaffLoginPage.as_view(), name="web-staff-login"),
    path("signup/", SignUpPage.as_view(), name="web-signup"),
    path("staff/signup/", StaffSignUpPage.as_view(), name="web-staff-signup")
]