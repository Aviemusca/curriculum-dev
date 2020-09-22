from django.urls import reverse
from utils.slugs import unique_slugify
from django.db import models
from django_countries.fields import CountryField

from accounts.models import CustomUser


class Curriculum(models.Model):
    """

    A class to manage curricula in the context of learning outcome
    analysis.

    """
    title = models.CharField(max_length=200)
    public = models.BooleanField(default=False)
    country = CountryField(blank_label='(select country)')
    isced_level = models.CharField(max_length=100, default='')
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='curricula')
    date_created = models.DateTimeField(auto_now_add=True)
    slug = models.SlugField(max_length=200, unique=True, blank=True)


    class Meta:


        verbose_name = 'Curriculum'
        verbose_name_plural = 'Curricula'


    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        slug_str = f"{self.author.username} {self.title}"
        unique_slugify(self, slug_str)
        super(Curriculum, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('curricula:detail', kwargs={'slug_curriculum': self.slug})

    def get_num_strands(self):
        """ Returns the current number of strands saved in the curriculum"""
        return self.strands.all().count()

    def has_strand(self):
        """ Returns True if the curriculum has at least one strand """
        return True if self.get_num_strands() > 0 else False

    def get_num_learning_outcomes(self):
        """ Returns the current number of learning outcomes in the curriculum """
        return sum(strand.get_num_learning_outcomes() for strand in self.strands.all())

    def get_num_analyses(self):
        """ Returns the number of analyses effectuated on the curriculum """
        return self.curriculum_analyses.all().count()

    def has_analysis(self):
        """ Returns True if the curriculum has at least one analysis """
        return True if self.get_num_analyses() > 0 else False
