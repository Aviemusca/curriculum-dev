from django.db.models.signals import post_save
from django.dispatch import receiver

#from .models import CurriculumAnalysis
#from .tasks import analyse_curriculum
#
#@receiver(post_save, sender=CurriculumAnalysis)
#def trigger_curriculum_analysis(sender, instance, created, **kwargs):
#    """ Signal to generate all analyses for a curriculum when user submits curriculum analysis form """
#    if created:
#        analyse_curriculum.delay(instance.pk)
#

