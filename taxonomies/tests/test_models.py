from django.test import TestCase

from django.urls import reverse
from django.contrib.auth import get_user_model

from taxonomies.models import CustomUserTaxonomy as Taxonomy
from verb_categories.models import VerbCategory
from verbs.models import Verb


class TaxonomyModelTests(TestCase):

    fixtures = [
            "yvan.json",
            "blooms_updated.json",
            "blooms_updated_knowledge.json",
            "blooms_updated_comprehension.json",
            "blooms_updated_application.json",
            "blooms_updated_analysis.json",
            "blooms_updated_synthesis.json",
            "blooms_updated_evaluation.json",
            ]

    def setUp(self):
        # Load fixtures:

        # Author of taxonomy:
        self.author = get_user_model().objects.get(pk=1)
        # Taxonomy
        self.tax = Taxonomy.objects.get(pk=1)
        # Verb categories
        self.verb_categories = [VerbCategory.objects.get(pk=index) for index in range(1, 7)]

    def test_author_loaded(self):
        self.assertEqual(self.author.username, 'yvan')

    def test_taxonomy_loaded(self):
        self.assertEqual(self.tax.title, 'Blooms updated')

    def test_categories_loaded(self):
        self.assertEqual(VerbCategory.objects.count(), 6)

    def test_str(self):
        self.assertEqual(str(self.tax), self.tax.title)

    def test_get_absolute_url(self):
        self.assertEqual(self.tax.get_absolute_url(), f'/taxonomies/taxonomy/{self.tax.slug}/')

    def test_get_num_verb_categories(self):
        self.assertEqual(self.tax.get_num_verb_categories(), 6)

    def test_get_num_verbs(self):
        # Create verb objects
        for verb_category in self.tax.verb_categories.all():
            cleaned_verbs = verb_category.get_cleaned_verbs()
            verb_category.generate_verb_objects(cleaned_verbs)
        self.assertEqual(self.tax.get_num_verbs(), 150)



