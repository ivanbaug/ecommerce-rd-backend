from django.db.models.signals import pre_save
from django.contrib.auth.models import User


def update_user(sender, instance, **kwargs):
    print("Signal triggered: Update User")
    user = instance
    if user.email != "":
        user.username = user.email


pre_save.connect(update_user, sender=User)
