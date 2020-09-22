from django.test import TestCase

from django.urls import reverse
from django.contrib.auth import get_user_model

from curricula.models import Curriculum
from strands.models import Strand
from learning_outcomes.models import LearningOutcome
from taxonomies.models import CustomUserTaxonomy as Taxonomy
from analyses.models import CurriculumAnalysis

class CurriculumTests(TestCase):

    fixtures = [
            "yvan.json",
            "CS.json",
            "CS_strand_1.json",     # pk=1
            "CS_strand_2.json",     # pk=2
            "CS_strand_3.json",     # pk=3
            "blooms_updated.json",
            ]

    def setUp(self):
        # Get Fixture objects

        # Author
        self.author = get_user_model().objects.get(pk=1)
        # Curriculum
        self.curriculum = Curriculum.objects.get(pk=1)
        # Strands
        self.strands = [Strand.objects.get(pk=index) for index in range(1, 4)]
        # Taxonomy
        self.taxonomy = Taxonomy.objects.get(pk=1)

        # Create 2 curriculum analyses
        self.analysis_1_params = {
                'title': 'test_analysis_1',
                'taxonomy': self.taxonomy,
                'curriculum': self.curriculum,
                }
        self.analysis_2_params = {
                'title': 'test_analysis_2',
                'taxonomy': self.taxonomy,
                'curriculum': self.curriculum,
                }
        self.analysis_1 = CurriculumAnalysis.objects.create(**self.analysis_1_params)
        self.analysis_2 = CurriculumAnalysis.objects.create(**self.analysis_2_params)

    def test_str(self):
        self.assertEqual(str(self.curriculum), self.curriculum.title)

    def test_get_absolute_url(self):
        url = self.curriculum.get_absolute_url()
        self.assertEqual(url, f"/curricula/curriculum/{self.curriculum.slug}/")

    def test_get_num_strands(self):
        self.assertEqual(self.curriculum.get_num_strands(), 3)

    def test_has_strand(self):
        self.assertTrue(self.curriculum.has_strand())

    def test_get_num_learning_outcomes(self):
        self.assertEqual(self.curriculum.get_num_learning_outcomes(), 59)

    def test_num_analyses(self):
        self.assertEqual(self.curriculum.get_num_analyses(), 2)

    def test_has_analysis(self):
        self.assertTrue(self.curriculum.has_analysis())
