from django.db import models
from users.models import User
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from .fields import OrderField
from django.utils.text import slugify
from django.template.loader import render_to_string
from django.urls import reverse
from decouple import config
from django.shortcuts import get_object_or_404
from django.core.validators import FileExtensionValidator
from .validator import validate_file_size
from django.template.loader import render_to_string
from django.utils.encoding import smart_bytes
from django.utils.html import strip_tags
from django.core.mail import send_mail

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
    owner = models.ForeignKey(User, related_name='courses_created', on_delete=models.CASCADE, limit_choices_to={"is_lecturer":True})
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
    requirements = models.TextField(blank=True, null=True)

    # def get_students_enrolled(course_slug):
    #     course = get_object_or_404(Course, slug=course_slug)
    #     students = course.students.all()
    #     return students
    
    def get_students_enrolled(self):
        return self.students.all()


    class Meta:
        ordering = ['-created']

    def save(self, *args, **kwargs):
        if not self.slug:
            compound_slug = str(self.title)
            self.slug = slugify(compound_slug)
        super().save(*args, **kwargs)

    def num_enrolled_students(self):
        return self.students.count()
    
    def get_absolute_url(self):
        return reverse('course-detail', kwargs={'slug': self.slug})



    def __str__(self):
        return self.title
    

class CourseMaterials(models.Model):
    course = models.ForeignKey(Course, related_name='course_materials', on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    description = models.TextField()
    file = models.FileField(upload_to="course_materials", validators=[
        FileExtensionValidator(allowed_extensions=['pdf', 'doc', 'docx']),  # Example allowed file extensions
         validate_file_size,  # 5 MB limit (in bytes)
    ])
    url = models.URLField(blank=True, null=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return self.title
    
    class Meta:
        verbose_name_plural = "Course Materials"
    

    

class Enrollment(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    student = models.ForeignKey(User, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.course.title
    
    
    


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




class Broadcast(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    subject = models.CharField(max_length=150)
    message = models.TextField()
    creator = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={'is_staff': True})
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.subject
    
    # def save(self, *args, **kwargs):
    #     super().save(*args, **kwargs)
    #     # Send broadcast message to all students in the course
    #     students = self.course.get_students_enrolled()
    #     for student in students:
    #         # Implement your notification or messaging mechanism here
    #         # For example, sending an email to each student
    #         # You might need to adjust this part based on your actual notification method
    #         self.send_notification_to_student(student)

    # def send_notification_to_student(self, student):
        # # Implement your notification method here, e.g., sending an email
        # # Example implementation using Django's EmailMessage:
        # from django.core.mail import send_mail
        # subject = f"New Broadcast: {self.subject}"
        # message = f"Dear {student.username},\n\n{self.message}\n\nSincerely,\nThe Administration"
        # sender_email = config('EMAIL_HOST_USER')
        # send_mail(subject, message, sender_email, [student.email])


        # import mailtrap as mt

        # # create mail object
        # mail = mt.Mail(
        #     sender=mt.Address(email="mailtrap@demomailtrap.com", name="Mailtrap Test"),
        #     to=[mt.Address(email=student.email)],
        #     subject=self.subject,
        #     text=self.message,
        # )

        # # create client and send
        # client = mt.MailtrapClient(token=config("MAILTRAP_TOKEN"))
        # client.send(mail)

        subject = self.subject
        message = render_to_string('courses/course/email_notification.html', {"message": self.message})
        plain_message = strip_tags(message)
        recipients = [student.email]
        send_mail(subject, plain_message, config('DEFAULT_FROM_EMAIL'), recipients)

    
