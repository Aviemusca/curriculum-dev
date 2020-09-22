from django.urls import reverse
from utils.slugs import unique_slugify

from django.db import models

from accounts.models import CustomUser
from taxonomies.models import CustomUserTaxonomy
from verbs.models import Verb, NonVerb

from utils.get import VerbCategoryMixin


class VerbCategory(models.Model, VerbCategoryMixin):
    """

    A class to manage the verb categories of a given taxonomy.
    The level field represents the level of abstraction of the
    verb category within the taxonomy, e.g. in Bloom Knowledge=1
    Comprehension=2, ..., Evaluation=6

    """

    title = models.CharField(max_length=100)
    date_created = models.DateTimeField(auto_now_add=True)
    level = models.PositiveIntegerField(default=1)
    taxonomy = models.ForeignKey(CustomUserTaxonomy, on_delete=models.CASCADE, related_name='verb_categories')
    verb_list = models.TextField(default='')
    slug = models.SlugField(max_length=150, blank=True, unique=True)

    class Meta:
        verbose_name = 'Verb Category'
        verbose_name_plural = 'Verb Categories'
        unique_together = ('taxonomy', 'level')

    def __str__(self):
        return self.title

    def __len__(self):
        """ Make the length of a category equal to the number of verbs and allowed non-verbs """
        return self.get_num_verbs() + self.get_num_non_verbs()

    def __add__(self, other):
        """ Adding 2 categories returns the union of elements """
        verbs = [verb.title for verb in self.verbs.all()] + [verb.title for verb in other.verbs.all()]
        non_verbs = [verb.title for verb in self.non_verbs.all()] + [verb.title for verb in other.non_verbs.all()]
        return set(verbs + non_verbs)

    def __mul__(self, other):
        """ Multiplying 2 categories returns the interstecting/overlapping verbs  """
        return set(verb.title for verb in self.verbs.all()) & set(verb.title for verb in other.verbs.all())

    #def __eq__(self, other):
    #    """ 2 categories are equal if all their elements are the same """
    #    return set(self.verbs.all()) == set(other.verbs.all()) and set(self.non_verbs.all()) == set(other.non_verbs.all())

    def get_absolute_url(self):
        return reverse('taxonomies:verb_categories:detail', kwargs={'pk_taxonomy': self.get_taxonomy_pk(), 'slug_taxonomy': self.get_taxonomy_slug(),  'slug_verb_category': self.slug})

    def save(self, *args, **kwargs):
        created = self.pk is None
        slug_str = f"{self.taxonomy.pk} {self.title}"
        unique_slugify(self, slug_str)
        super().save(*args, **kwargs)
        if created or not self._state.adding: # Second for updating
            cleaned_verbs = self.get_cleaned_verbs()
            self.generate_verb_objects(cleaned_verbs)

    def get_taxonomy(self):
        return self.taxonomy

    def get_author(self):
        """ Returns the author of the verb category/taxonomy """
        return self.taxonomy.author

    def get_cleaned_verbs(self):
        """ Returns a list of cleaned text learning outcome strings """
        return self.verb_list.lower().replace(' ', '').strip().split(',')

    def generate_verb_objects(self, cleaned_verbs):
        """ Generates a collection of verb objects from a list of verbs """

        # Filter out the allowed non verbs, i.e. terms with surrounding parentheses
        allowed_non_verbs = self.filter_non_verbs(cleaned_verbs)
        # Remove the non_verbs from the cleaned_verbs
        cleaned_verbs = self.remove_non_verbs(cleaned_verbs, allowed_non_verbs)

        # Remove (not delete as many-to-many field) any pre-existing verbs from the verb category
        for verb in self.verbs.all():
            self.verbs.remove(verb)
        # Remove (not delete as many-to-many field) any pre-existing non_verbs from the verb category
        for non_verb in self.non_verbs.all():
            self.non_verbs.remove(non_verb)

        # Create or add the verb and non_verb objects
        for non_verb in allowed_non_verbs:
            self.add_non_verb(non_verb)
        for verb in cleaned_verbs:
            self.add_verb(verb)

    def add_non_verb(self, non_verb_text):
        """ Creates a non_verb object and attaches it to the verb category """
        non_verb_text = non_verb_text.lower()

        # Create new object if it does not exist in the db
        if non_verb_text not in [non_verb.title for non_verb in NonVerb.objects.all()]:
            new_non_verb = NonVerb.objects.create(title=non_verb_text)
            new_non_verb.verb_categories.add(self)
        # If it exists in another category, connect it with the current category
        elif non_verb_text not in [non_verb.title for non_verb in self.non_verbs.all()]:
            target_non_verb = NonVerb.objects.filter(title=non_verb_text).first()
            target_non_verb.verb_categories.add(self)
        else:
            pass

    def add_verb(self, verb_text):
        """ Creates a verb object and attaches it to the verb category """
        verb_text = verb_text.lower()
        if verb_text not in [verb.title for verb in Verb.objects.all()]:
            new_verb = Verb.objects.create(title=verb_text)
            new_verb.verb_categories.add(self)
        elif verb_text not in [verb.title for verb in self.verbs.all()]:
            target_verb = Verb.objects.filter(title=verb_text).first()
            target_verb.verb_categories.add(self)
        else:
            pass

    def has_verb(self):
        """ Retruns true if a verb exists in the db else false """
        return True if self.verbs.count() > 0 else False

    def has_non_verb(self):
        """ Retruns true if an allowed non_verb exists in the db else false """
        return True if self.non_verbs.count() > 0 else False

    def get_num_verbs(self):
        """ Returns the number of verbs in the verb category """
        return self.verbs.count()

    def get_num_non_verbs(self):
        """ Returns the number of allowed non-verbs in the verb category """
        return self.non_verbs.count()

    def get_num_elements(self):
        """ Returns the number of verbs and allowed non-verbs in the verb category """
        return self.verbs.count() + self.non_verbs.count()

    def filter_non_verbs(self, cleaned_verbs):
        """ Returns a list of allowed non-verbs from the cleaned verb_list. These are flagged
        by enclosing parentheses """
        return [verb[1:-1] for verb in cleaned_verbs if (verb[0] == '(' and verb[-1] == ')')]

    def remove_non_verbs(self, cleaned_verbs, allowed_non_verbs):
        """ Removes the allowed non-verbs from the cleaned_verbs """
        # Remove parentheses from cleaned_verbs
        cleaned_verbs = ','.join(cleaned_verbs).replace('(', '').replace(')', '').split(',')
        # Return cleaned_verbs without allowed non-verbs
        return [verb for verb in cleaned_verbs if verb not in allowed_non_verbs]

    def get_verbs_string(self):
        """ Returns the verbs of the category as a string """
        return ', '.join([verb.title for verb in self.verbs.all()])

    def get_non_verbs_string(self):
        """ Returns the allowed non-verbs of the category as a string """
        return ', '.join([non_verb.title for non_verb in self.non_verbs.all()])

    def get_elements_string(self):
        """ Returns the verbs and allowed non-verbs of the category as a string """
        return self.get_verbs_string() + ', ' + self.get_non_verbs_string()

    def overlap(self, other):
        """ Returns the number of verbs appearing simulataneously in 2 different categories """
        return len(self * other)

    def diagonal_verbs(self):
        """ Returns the number of verbs appearing exclusively in the category """
        return sum(self.overlap(other) if self == other else -self.overlap(other) \
                for other in self.taxonomy.verb_categories.all())
