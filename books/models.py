from django.db import models
import uuid
from django.utils.text import slugify
from courses.models import Course


class Book(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, max_length=36)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    slug = models.SlugField(max_length=300, blank=True)
    title = models.CharField(max_length=300)
    author = models.CharField(max_length=200)
    vote_count = models.IntegerField()
    vote_average = models.DecimalField(max_digits=4, decimal_places=1)
    published_date = models.DateField()


    def __str__(self):
        return self.title
    
    
    # def save(self, *args, **kwargs):
    #     if not self.slug:
    #         self.slug = slugify(self.title)
    #         super().save(*args, **kwargs)


