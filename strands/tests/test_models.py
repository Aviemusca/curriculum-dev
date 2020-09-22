from django.test import TestCase

from django.urls import reverse
from django.contrib.auth import get_user_model

from curricula.models import Curriculum
from strands.models import Strand
from learning_outcomes.models import LearningOutcome
from taxonomies.models import CustomUserTaxonomy as Taxonomy
from analyses.models import CurriculumAnalysis

class StrandTests(TestCase):

    fixtures = [ # All have pk=1
            "yvan.json",
            "CS.json",
            "CS_strand_1.json",
            ]
    def setUp(self):
        # Get fixture objects

        # Author
        self.author = get_user_model().objects.get(pk=1)
        # Curriculum
        self.curriculum = Curriculum.objects.get(pk=1)
        # Strand
        self.strand = Strand.objects.get(pk=1)

    def test_str(self):
        self.assertEqual(str(self.strand), self.strand.title)

    def test_post_save_signal(self):
        num_los = LearningOutcome.objects.filter(strand=self.strand).count()
        self.assertEqual(num_los, 23)

    def test_get_absolute_url(self):
        url = self.strand.get_absolute_url()
        self.assertEqual(url, f"/curricula/curriculum/{self.curriculum.slug}/strands/{self.curriculum.pk}/strand/{self.strand.slug}/")

    def test_get_curriculum(self):
        self.assertEqual(self.strand.get_curriculum(), self.strand.curriculum)

    def test_get_author(self):
        self.assertEqual(self.strand.get_author(), self.strand.curriculum.author)

    def test_get_cleaned_learning_outcomes(self):
        self.assertEqual(len(self.strand.get_cleaned_learning_outcomes()), 23)

    def test_pre_existing_learning_outcome(self):
        cleaned_lo = self.strand.get_cleaned_learning_outcomes()[0]
        self.strand.add_learning_outcome(cleaned_lo)
        num_los = LearningOutcome.objects.filter(strand=self.strand).count()
        self.assertEqual(num_los, 23) # should still be 23

    def test_add_new_learning_outcome(self):
        new_lo = "Should be able to sleep soundly at night"
        self.strand.add_learning_outcome(new_lo)
        num_los = LearningOutcome.objects.filter(strand=self.strand).count()
        self.assertEqual(num_los, 24)

    def test_generate_learning_outcomes(self):
        new_los = ["Left alone", "reminded about saturday", "Can use skills of logic"]
        self.strand.generate_learning_outcomes(new_los)
        num_los = LearningOutcome.objects.filter(strand=self.strand).count()
        self.assertEqual(num_los, 3)

    def test_get_num_learning_outcomes(self):
        self.assertEqual(self.strand.get_num_learning_outcomes(), 23)

    def test_has_learning_outcome(self):
        self.assertTrue(self.strand.has_learning_outcome())



