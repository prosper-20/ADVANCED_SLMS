from django.db import models
from users.models import User
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from .fields import OrderField
from django.utils.text import slugify
from django.template.loader import render_to_string
from django.urls import reverse


class Subject(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True)

    class Meta:
        ordering = ['title']

    def __str__(self):
        return self.title
    
YEAR = (
    ("Year 1", "Year 1"),
    ("Year 2", "Year 2"),
    ("Year 3", "Year 3"),
    ("Year 4", "Year 4"),
    ("Year 5", "Year 5"),
)

SEMESTER = (
    ("First Semester", "First Semester"),
    ("Second Semester", "Second Semester")
)

COURSE_MODE_CHOICES = (
    ('Physical', 'Physical'),
    ('Online', 'Online')
)

class Course(models.Model):
    owner = models.ForeignKey(User, related_name='courses_created', on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject, related_name='courses', on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    code = models.CharField(max_length=100, blank=True, null=True)
    slug = models.SlugField(max_length=200, unique=True, blank=True)
    image = models.ImageField(default="course.jpg", upload_to="course_image")
    overview = models.TextField()
    year = models.CharField(default="Year 5", choices=YEAR, max_length=100)
    semester = models.CharField(default="First Semester", choices=SEMESTER, max_length=100)
    students = models.ManyToManyField(User, related_name='courses_joined', blank=True)
    created = models.DateTimeField(auto_now_add=True)
    mode = models.CharField(default="Physical", choices=COURSE_MODE_CHOICES, max_length=30)
    duration = models.TextField(default="12 weeks")

    class Meta:
        ordering = ['-created']

    def save(self, *args, **kwargs):
        if not self.slug:
            compound_slug = str(self.subject.title) + "-" + str(self.title)
            self.slug = slugify(compound_slug)
        super().save(*args, **kwargs)

    def num_enrolled_students(self):
        return self.students.count()
    
    def get_absolute_url(self):
        return reverse('course-detail', kwargs={'slug': self.slug})



    def __str__(self):
        return self.title
    


class Module(models.Model):
    course = models.ForeignKey(Course, related_name='modules', on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    order = OrderField(blank=True, for_fields=['course'])

    class Meta:
        ordering = ['order']


    def __str__(self):
        return f'{self.order}. {self.title}'
    

class Content(models.Model):
    module = models.ForeignKey(Module,related_name='contents', on_delete=models.CASCADE)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, limit_choices_to={'model__in':('text','video','image','file')})
    object_id = models.PositiveIntegerField()
    item = GenericForeignKey('content_type', 'object_id')
    order = OrderField(blank=True, for_fields=['module'])

    class Meta:
        ordering = ['order']


class ItemBase(models.Model):
    owner = models.ForeignKey(User, related_name='%(class)s_related', on_delete=models.CASCADE)
    title = models.CharField(max_length=250)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

    def __str__(self):
        return self.title
    
    def render(self):
        return render_to_string(
        f'courses/content/{self._meta.model_name}.html',
        {'item': self})

class Text(ItemBase):
    content = models.TextField()

class File(ItemBase):
    file = models.FileField(upload_to='files')

class Image(ItemBase):
    file = models.FileField(upload_to='images')

class Video(ItemBase):
    url = models.URLField()
