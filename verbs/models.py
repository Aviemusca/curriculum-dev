from django.db import models
from utils.slugs import unique_slugify

class Verb(models.Model):
    """

    A class to manage the verbs of a verb category.

    """

    title = models.CharField(max_length=100)
    date_created = models.DateTimeField(auto_now_add=True)
    verb_categories = models.ManyToManyField('verb_categories.VerbCategory', related_name='verbs')
    slug = models.SlugField(max_length=150, blank=True, unique=True)


    class Meta:
        verbose_name = 'Verb'
        verbose_name_plural = 'Verbs'


    def __str__(self):
        return self.title

    def get_absolute_url(self):
        pass

    def save(self, *args, **kwargs):
        slug_str = f"{self.title}"
        unique_slugify(self, slug_str)
        super(Verb, self).save(*args, **kwargs)


class NonVerb(models.Model):
    """

    A class to manage the allowed non-verbs of a verb category, e.g. "who, what.." in the 'knowledge'
    category of Blooms taxonomy.

    """
    title = models.CharField(max_length=100)
    date_created = models.DateTimeField(auto_now_add=True)
    verb_categories = models.ManyToManyField('verb_categories.VerbCategory', related_name='non_verbs')
    slug = models.SlugField(max_length=150, blank=True, unique=True)


    class Meta:
        verbose_name = 'Non Verb'
        verbose_name_plural = 'Non Verbs'


    def __str__(self):
        return self.title

    def get_absolute_url(self):
        pass

    def save(self, *args, **kwargs):
        slug_str = f"{self.title}"
        unique_slugify(self, slug_str)
        super(NonVerb, self).save(*args, **kwargs)


class NonCatVerb(models.Model):
    """

    A class to manage the non-categorised verbs in a curriculum analysis

    """
    title = models.CharField(max_length=100)
    date_created = models.DateTimeField(auto_now_add=True)
    curriculum_analyses = models.ManyToManyField('analyses.CurriculumAnalysis', related_name='non_cat_verbs')
    slug = models.SlugField(max_length=150, blank=True, unique=True)


    class Meta:
        verbose_name = 'Non Categorised Verb'
        verbose_name_plural = 'Non Categorised Verbs'


    def __str__(self):
        return self.title

    def get_absolute_url(self):
        pass

    def save(self, *args, **kwargs):
        slug_str = f"{self.title}"
        unique_slugify(self, slug_str)
        super(NonCatVerb, self).save(*args, **kwargs)


