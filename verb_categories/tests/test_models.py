from django.test import TestCase

from django.urls import reverse
from django.contrib.auth import get_user_model

from taxonomies.models import CustomUserTaxonomy as Taxonomy
from verb_categories.models import VerbCategory
from verbs.models import Verb


class VerbCategoryModelTests(TestCase):

    fixtures = [ # All have pk=1
            "yvan.json",
            "blooms_updated.json",
            "blooms_updated_knowledge.json",
            ]

    def setUp(self):
        # Get fixture objects

        # Author of taxonomy
        self.author = get_user_model().objects.get(pk=1)
        # Taxonomy
        self.tax = Taxonomy.objects.get(pk=1)
        # Verb category
        self.verb_cat = VerbCategory.objects.get(pk=1)

    def test_str(self):
        self.assertEqual(str(self.verb_cat), self.verb_cat.title)

    def test_get_absolute_url(self):
        self.assertEqual(self.verb_cat.get_absolute_url(), f'/taxonomies/taxonomy/{self.tax.slug}/verb_categories/{self.tax.pk}/verb_category/{self.verb_cat.slug}/')

    def test_post_save_signal(self):
        # Number of verb objects created should be 22
        num_verbs = Verb.objects.filter(verb_categories=self.verb_cat).count()
        self.assertEqual(num_verbs, 22)

    def test_get_taxonomy_title(self):
        self.assertEqual(self.verb_cat.get_taxonomy_title(), self.tax.title)

    def test_get_taxonomy_pk(self):
        self.assertEqual(self.verb_cat.get_taxonomy_pk(), self.tax.pk)

    def test_get_taxonomy_slug(self):
        self.assertEqual(self.verb_cat.get_taxonomy_slug(), self.tax.slug)

    def test_get_author(self):
        self.assertEqual(self.verb_cat.get_author(), self.tax.author)

    def test_get_author_pk(self):
        self.assertEqual(self.verb_cat.get_author_pk(), self.tax.author.pk)

    def test_get_author_username(self):
        self.assertEqual(self.verb_cat.get_author_username(), self.tax.author.username)

    def test_get_cleaned_verbs(self):
        self.assertEqual(self.verb_cat.get_cleaned_verbs(), self.verb_cat.verb_list.lower().replace(' ', '').strip().split(','))

    def test_add_verb_increases_num_verbs(self):
        # Number of verbs originally 22
        verb_txt = "think"
        self.verb_cat.add_verb(verb_txt)
        num_verbs = Verb.objects.filter(verb_categories=self.verb_cat).count()
        self.assertEqual(num_verbs, 23)

    def test_add_verb(self):
        verb_txt = "think"
        self.verb_cat.add_verb(verb_txt)
        verb = Verb.objects.filter(verb_categories=self.verb_cat).filter(title=verb_txt)
        self.assertTrue(verb)

    def test_add_pre_existing_verb(self):
        pre_existing_verb = self.verb_cat.get_cleaned_verbs()[0]
        self.verb_cat.add_verb(pre_existing_verb)
        num_verbs = Verb.objects.filter(verb_categories=self.verb_cat).count()
        self.assertEqual(num_verbs, 22)

    def test_generate_verb_objects_deletes_pre_existing_verbs(self):
        cleaned_verbs = ["read", "think", "forsee"] # read already in so should just add 2
        self.verb_cat.generate_verb_objects(cleaned_verbs)
        num_verbs = Verb.objects.filter(verb_categories=self.verb_cat).count()
        self.assertEqual(num_verbs, 24)

    def test_get_num_verbs(self):
        self.assertEqual(self.verb_cat.get_num_verbs(), 22)
