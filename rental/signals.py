from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

from .constants import TeamEnum
from .models import Personnel, Team


@receiver(post_save, sender=User)
def create_personnel_profile(sender, instance, created, **kwargs):
    if created:
        try:
            # Assign default team
            default_team = Team.objects.get(name=TeamEnum.NOTEAM.value)
        except Team.DoesNotExist:
            default_team = None  # Handle accordingly if the team doesn't exist
        Personnel.objects.create(user=instance, team=default_team)


@receiver(post_save, sender=User)
def save_personnel_profile(sender, instance, **kwargs):
    try:
        instance.personnel.save()
    except Personnel.DoesNotExist:
        # If Personnel doesn't exist, create one with default team
        default_team = Team.objects.get(name=TeamEnum.NOTEAM.value)
        Personnel.objects.create(user=instance, team=default_team)
