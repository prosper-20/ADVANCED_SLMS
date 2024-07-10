from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.utils import timezone
from .models import Broadcast



# @receiver(pre_save, sender=Broadcast)
# def set_broadcast_creator(sender, instance, **kwargs):
#     if instance.creator is None:
#         # Assuming you have middleware to set request.user properly
#         from django.contrib.auth import get_user_model
#         User = get_user_model()
#         user = User.objects.filter(username='ethos')
#         instance.creator = user