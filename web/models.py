from django.db import models
from users.models import User

class Post(models.Model):
    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=55)
    image = models.ImageField(default="post.jpg", upload_to="post_images")
    content = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title


