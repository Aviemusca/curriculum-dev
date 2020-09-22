from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import VerbCategory

@receiver(post_save, sender=VerbCategory)
def create_verbs(sender, instance, created, **kwargs):
    if created:
        cleaned_verbs = instance.get_cleaned_verbs()
        instance.generate_verb_objects(cleaned_verbs)
