from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


@receiver(post_save, sender=User)
def create_user_with_profile(sender, instance, created, **kwargs):
    print("create_user_with_profile")
