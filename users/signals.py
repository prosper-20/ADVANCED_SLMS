from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model

User = get_user_model()

@receiver(post_save, sender=User)
def create_profile(sender, created, instance, **kwargs):
    if created:
        User.objects.create(user=instance)



@receiver(post_save, sender=User) 
def save_lecturer_profile(sender, instance, **kwargs):
        instance.profile.save()




        