from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from .managers import CustomUserManager


TITLE = (
    ("Engr.", "Engr."),
    ("Prof.", "Prof"),
    ("Dr.", "Dr.")
)


class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=200, unique=True)
    title = models.CharField(max_length=100, choices=TITLE, default="Engr.")
    email = models.EmailField(_("email address"), unique=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_lecturer = models.BooleanField(default=False)
    date_joined = models.DateTimeField(default=timezone.now)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.email
    
    def get_full_name(self):
        return self.username
    

    


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to="profile_pictures", default="user.jpg")
    bio = models.TextField()

    def __str__(self):
        return f"{self.user.title} {self.user.username}"
    

