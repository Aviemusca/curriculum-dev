from django.urls import reverse
from utils.slugs import unique_slugify

from django.db import models

from utils.get import CurriculumGetMethods, AuthorGetMethods

from accounts.models import CustomUser
from curricula.models import Curriculum
from learning_outcomes.models import LearningOutcome

class Strand(models.Model, CurriculumGetMethods, AuthorGetMethods):
    """

    A class to manage the learning outcome strands of a curriculum.
    A curriculum is connected with a collection of strands which are tied to no other curriculum.

    """

    title = models.CharField(max_length=200)
    curriculum = models.ForeignKey(Curriculum, on_delete=models.CASCADE, related_name='strands')
    date_created = models.DateTimeField(auto_now_add=True)
    colour = models.CharField(max_length=7, default='#444444')
    learning_outcome_list = models.TextField(default='')
    slug = models.SlugField(max_length=200, unique=True, blank=True)


    class Meta:
        verbose_name = 'Strand'
        verbose_name_plural = 'Strands'


    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        created = self.pk is None
        slug_str = f"{self.curriculum.pk} {self.title}"
        unique_slugify(self, slug_str)
        super(Strand, self).save(*args, **kwargs)
        if created or not self._state.adding: # Second for updating
            cleaned_learning_outcomes = self.get_cleaned_learning_outcomes()
            self.generate_learning_outcomes(cleaned_learning_outcomes)


    def get_absolute_url(self):
        return reverse('curricula:strands:detail', kwargs={'pk_curriculum': self.get_curriculum_pk(), 'slug_curriculum': self.get_curriculum_slug(),  'slug_strand': self.slug})

    def get_curriculum(self):
        """ Returns the title of the strands' curriculum """
        return self.curriculum

    def get_author(self):
        """ Returns the author of the strands' curriculum """
        return self.get_curriculum().author

    def get_cleaned_learning_outcomes(self):
        """ Returns a list of cleaned text learning outcome strings """
        learning_outcomes = self.learning_outcome_list.split('\r\n')
        return learning_outcomes

    def generate_learning_outcomes(self, cleaned_learning_outcomes):
        """ Deletes any pre-existing LOs in the strand and creates a fresh collection of LOs from a cleaned LO list """
        LearningOutcome.objects.filter(strand=self).delete()
        for learning_outcome in cleaned_learning_outcomes:
            self.add_learning_outcome(learning_outcome)

    def add_learning_outcome(self, learning_outcome_text):
        """ Creates a learning outcome object and appends it to the strand """
        # Ensure LO is not already in the strand
        LO_queryset = LearningOutcome.objects.filter(strand=self)
        if learning_outcome_text not in [LO.text for LO in LO_queryset]:
            LearningOutcome.objects.create(index=LO_queryset.count()+1, strand=self, text=learning_outcome_text)

    def remove_learning_outcome(self, index):
        """ Removes/destroys LO of a given index in the strand """
        pass

    def get_num_learning_outcomes(self):
        """ Returns the number of learning outcomes in the curriculum strand """
        return self.learning_outcomes.count()

    def has_learning_outcome(self):
        """ Returns True if the strand has at least 1 learning outcome """
        return True if self.get_num_learning_outcomes() > 0 else False


