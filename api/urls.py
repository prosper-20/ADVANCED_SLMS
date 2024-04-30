from django.urls import path
from .views import ApiStudentsCoursesListView, ApiStudentsDetailView, ApiStudentCourseEnrollView, ApiCourseListView, ApiUserRegistrationView

urlpatterns = [
    path("", ApiStudentsCoursesListView.as_view(), name="api-home"),
    path("all/", ApiCourseListView.as_view(), name="all_courses"),
    path("register/", ApiUserRegistrationView.as_view(), name="register"),
    path("<int:id>/<slug:slug>/", ApiStudentsDetailView.as_view(), name="api-detail"),
    path("<int:id>/<slug:slug>/enroll/", ApiStudentCourseEnrollView.as_view(), name="api-enroll"),

]