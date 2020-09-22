from django.db import models
from utils.slugs import unique_slugify
import spacy

class LearningOutcome(models.Model):
    """

    A class to manage the individual learning outcomes of a curriculum.
    Each learning outcome (LO) is connected with a unique Strand object
    and each strand is connected with a collection of LOs.

    fields:
        index: index of the LO within a strand.
        text: The raw text of the LO e.g. "Students can read..."

    """
    index = models.PositiveIntegerField(default=0)
    text = models.CharField(max_length=500)
    strand = models.ForeignKey('strands.Strand', on_delete=models.CASCADE, related_name='learning_outcomes')
    date_created = models.DateTimeField(auto_now_add=True)
    slug = models.SlugField(max_length=200, unique=True, blank=True)


    class Meta:


        verbose_name = 'Learning Outcome'
        verbose_name_plural = 'Learning Outcomes'

    def __str__(self):
        return self.text[:100]

    def save(self, *args, **kwargs):
        slug_str = f"{self.strand.title} {self.index}"
        unique_slugify(self, slug_str)
        super(LearningOutcome, self).save(*args, **kwargs)

    def get_absolute_url(self):
        pass

        return self.text


