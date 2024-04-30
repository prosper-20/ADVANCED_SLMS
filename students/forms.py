from django import forms
from courses.models import Course
from django.contrib.auth.forms import UserCreationForm
from users.models import User

class UserRegistrationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ["username", "password1", "password2"]

class CourseEnrollForm(forms.Form):
    course = forms.ModelChoiceField(queryset=Course.objects.all(), widget=forms.HiddenInput)