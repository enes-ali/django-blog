from django.db import models
from Main.models import *
from django.dispatch import receiver
from django.db.models.signals import post_save
from rest_framework.authtoken.models import Token


@receiver(post_save, sender=User)
def CreateTokens(sender, instance, created, **kwarg):
    if created:
        token = Token.objects.create(user=instance)


