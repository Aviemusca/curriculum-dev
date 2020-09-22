from django.db import models
from django.urls import reverse
from utils.slugs import unique_slugify

from accounts.models import CustomUser


class CustomUserTaxonomy(models.Model):
    """

    A class to manage custom user created verb taxonomies for analysing
    the learning outcomes of a curriculum.
    A taxonomy has a number of associated verb categories.
    Each Verb Category has a number of verbs which, individually, may
    appear across several verb categories.

    """

    title = models.CharField(max_length=100)
    date_created = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='custom_user_taxonomies')
    slug = models.SlugField(max_length=150, blank=True, unique=True)
    public = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)

    class Meta:
        verbose_name = 'User Taxonomy'
        verbose_name_plural = 'User Taxonomies'

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('taxonomies:detail', kwargs={'slug_taxonomy': self.slug})

    def save(self, *args, **kwargs):
        slug_str = f"{self.author.pk} {self.title}"
        unique_slugify(self, slug_str)
        if self.author.is_staff:
            self.is_staff = True
        super().save(*args, **kwargs)

    def get_num_verb_categories(self):
        """ Returns the number of verb categories in the taxonomy """
        return self.verb_categories.count()

    def get_num_verbs(self):
        """ Returns the total number of verbs in the taxonomy """
        return sum(verb_cat.get_num_verbs() for verb_cat in self.verb_categories.all())

    def get_num_non_verbs(self):
        """ Returns the total number of allowed non-verbs in the taxonomy """
        return sum(verb_cat.get_num_non_verbs() for verb_cat in self.verb_categories.all())

    def get_num_elements(self):
        """ Returns the total number of verbs and allowed non-verbs in the taxonomy """
        return sum(len(verb_cat) for verb_cat in self.verb_categories.all())

    def get_num_unique_elements(self):
        """ Returns the number of unique elements in the taxonomy """
        verbs = [verb.title for verb_cat in self.verb_categories.all() for verb in verb_cat.verbs.all()]
        non_verbs = [verb.title for verb_cat in self.verb_categories.all() for verb in verb_cat.non_verbs.all()]

        return len(set(verbs + non_verbs))

    def has_verb_category(self):
        """ Returns True if the taxonomy has at least one verb category """
        return self.verb_categories.all().count() > 0

    def overlap(self):
        """ Returns the number of time a verb appears simultaneously in 2 categories """
        return int(0.5 * sum(VC_i.overlap(VC_j) for VC_i in self.verb_categories.all()\
                for VC_j in self.verb_categories.all() if VC_i != VC_j))
