from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from django.utils import timezone
from .models import Broadcast
from decouple import config
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.encoding import smart_bytes
from django.utils.html import strip_tags

# @receiver(pre_save, sender=Broadcast)
# def set_broadcast_creator(sender, instance, **kwargs):
#     if instance.creator is None:
#         # Assuming you have middleware to set request.user properly
#         from django.contrib.auth import get_user_model
#         User = get_user_model()
#         user = User.objects.filter(username='ethos')
#         instance.creator = user


# @receiver(post_save, Broadcast)
# def send_broadcast_mails(sender, created, instance, **kwargs):
#     if created:
#         students = instance.course.get_students_enrolled()
#         subject = f'{instance.subject}'
#         user_message = instance.message
#         message = render_to_string('courses/course/email_notification.html', {"user_message": user_message})
#         plain_message = strip_tags(message)
#         recipients = [student.email for student in students]
#         send_mail(subject, plain_message, config('DEFAULT_FROM_EMAIL_2'), recipients)
        
