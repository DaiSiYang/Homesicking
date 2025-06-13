from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import User, UserProfile


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    """
    当用户创建时，自动创建用户资料
    """
    if created:
        UserProfile.objects.create(user=instance) 