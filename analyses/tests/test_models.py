from django.test import TestCase

from django.urls import reverse

from django.contrib.auth import get_user_model

from analyses.models import (
        CurriculumAnalysis,
        StrandAnalysis,
        LearningOutcomeAnalysis,
        LearningOutcomeCategoryHitCount,
        StrandCategoryHitCount,
        StrandCategoryDiversity,
        StrandAverage,
        )

from curricula.models import Curriculum
from strands.models import Strand
from learning_outcomes.models import LearningOutcome
from taxonomies.models import CustomUserTaxonomy as Taxonomy
from verb_categories.models import VerbCategory


class SetUp(TestCase):
    """ The setup method for all proceeding classes """

    fixtures = [
            "yvan.json",
            "CS.json",
            "CS_strand_1.json",
            "CS_strand_2.json",
            "CS_strand_3.json",
            "blooms_updated.json",
            "blooms_updated_knowledge.json",
            "blooms_updated_comprehension.json",
            "blooms_updated_application.json",
            "blooms_updated_analysis.json",
            "blooms_updated_synthesis.json",
            "blooms_updated_evaluation.json",
            ]
    def setUp(self):

        # Get fixture objects

        # Author
        self.author = get_user_model().objects.get(pk=1)
        # Curriculum
        self.curr = Curriculum.objects.get(pk=1)
        # Strands
        self.strands = [Strand.objects.get(pk=index) for index in range(1, 4)]
        # Taxonomy
        self.tax = Taxonomy.objects.get(pk=1)
        # Verb categories
        self.verb_cats = [VerbCategory.objects.get(pk=index) for index in range(1, 7)]

        # Create curriculum analysis
        self.curr_analysis_params = {
                'title': 'curriculum_analysis',
                'curriculum': self.curr,
                'taxonomy': self.tax,
                }
        self.curr_analysis = CurriculumAnalysis.objects.create(**self.curr_analysis_params)
        # Create strand analyses
        self.strand_analyses = [StrandAnalysis.objects.create(title=f"strand_analysis_{strand.title}", curriculum_analysis=self.curr_analysis, strand=strand) for strand in self.strands]

#        # Create LO analyses
#        self.los = LearningOutcome.objects.filter(strand=self.strand).all()
#        self.lo_analyses = []
#        for index, lo in enumerate(self.los):
#            lo_analysis_params = {
#                'index': index+1,
#                'strand_analysis': self.strand_analysis,
#                'learning_outcome': lo,
#                }
#            lo_analysis = LearningOutcomeAnalysis.objects.create(**lo_analysis_params)
#            self.lo_analyses.append(lo_analysis)


class TestCurriculumAnalysis(SetUp):

    def test_str(self):
        self.assertEqual(str(self.curr_analysis), self.curr_analysis.title)

    def test_get_absolute_url(self):
        self.assertEqual(self.curr_analysis.get_absolute_url(), f'/curricula/curriculum/{self.curr.slug}/analyses/{self.curr.pk}/{self.curr_analysis.slug}/')

    def test_get_curriculum(self):
        self.assertEqual(self.curr_analysis.get_curriculum(), self.curr)

    def test_get_taxonomy(self):
        self.assertEqual(self.curr_analysis.get_taxonomy(), self.tax)

    def test_get_author(self):
        self.assertEqual(self.curr_analysis.get_author(), self.author)

    def test_curriculum_hit_count_analysis(self):
        target_hit_counts = [[13, 10, 21, 7, 4, 6], [11, 11, 26, 8, 6, 4], [3, 6, 17, 2, 10, 3]] # The total number of verb hits for all 6 categories and 3 strands
        estimated_hit_counts = []
        self.curr_analysis.learning_outcome_category_hit_count_analyses()
        for index, strand_analysis in enumerate(self.curr_analysis.strand_analyses.all()):
            estimated_hit_counts.append([0 for _ in range(6)])
            lo_analyses = strand_analysis.learning_outcome_analyses.all()
            for lo_analysis in lo_analyses:
                lo_category_hit_counts = lo_analysis.learning_outcome_category_hit_counts.all()
                for cat_index, category in enumerate(self.verb_cats):
                    estimated_hit_counts[index][cat_index] += lo_category_hit_counts.get(category=category.title).hit_count
        self.assertEqual(estimated_hit_counts, target_hit_counts)

    def test_strand_category_hit_count_analyses(self):
        target_hit_counts = [[11, 9, 13, 7, 3, 6], [11, 9, 18, 8, 4, 3], [2, 6, 11, 2, 8, 3]] # The total number of LOs hitting each of the 6 categories in the 3 strands
        estimated_hit_counts = []
        self.curr_analysis.learning_outcome_category_hit_count_analyses()
        self.curr_analysis.strand_category_hit_count_analyses()
        for index, strand_analysis in enumerate(self.curr_analysis.strand_analyses.all()):
            estimated_hit_counts.append([0 for _ in range(6)])
            strand_cat_hit_counts = strand_analysis.strand_category_hit_counts.all()
            for cat_index, category in enumerate(self.verb_cats):
                estimated_hit_counts[index][cat_index] += strand_cat_hit_counts.get(category=category.title).hit_count
        self.assertEqual(estimated_hit_counts, target_hit_counts)

    def test_strand_diversity_hit_count_analyses(self):
        target_hit_counts = [[6, 11, 3, 3, 0, 0], [5, 7, 6, 4, 0, 0], [4, 5, 2, 3, 0, 0]] # The total number of LOs hitting each of the 6 categories in the 3 strands
        estimated_hit_counts = []
        self.curr_analysis.learning_outcome_category_hit_count_analyses()
        self.curr_analysis.strand_category_diversity_analyses()
        for index, strand_analysis in enumerate(self.curr_analysis.strand_analyses.all()):
            estimated_hit_counts.append([0 for _ in range(6)])
            strand_cat_diversity_hit_counts = StrandCategoryDiversity.objects.filter(strand_analysis=strand_analysis)
            for cat_index, category in enumerate(self.verb_cats):
                estimated_hit_counts[index][cat_index] = strand_cat_diversity_hit_counts.get(num_categories=cat_index+1).num_learning_outcomes
        self.assertEqual(estimated_hit_counts, target_hit_counts)

    def test_strand_average_analyses(self):
        target_verb_averages = [2.65, 3.0, 2.93] # The target average number of verbs in ach strand
        target_category_averages = [2.13, 2.41, 2.29] # The target average number of categories in each strand
        estimated_verb_averages = []
        estimated_category_averages = []
        self.curr_analysis.learning_outcome_category_hit_count_analyses()
        self.curr_analysis.strand_category_diversity_analyses()
        self.curr_analysis.strand_average_analyses()
        for index, strand_analysis in enumerate(self.curr_analysis.strand_analyses.all()):
            strand_average = StrandAverage.objects.get(strand_analysis=strand_analysis)
            estimated_category_averages.append(strand_average.categories)
            estimated_verb_averages.append(strand_average.verbs)
        self.assertEqual(estimated_verb_averages, target_verb_averages)
        self.assertEqual(estimated_category_averages, target_category_averages)




class TestStrandAnalysis(SetUp):

    def test_str(self):
        self.assertEqual(str(self.strand_analyses[0]), self.strand_analyses[0].title)

    def test_get_curriculum(self):
        self.assertEqual(self.strand_analyses[0].get_curriculum(), self.curr)

    def test_get_taxonomy(self):
        self.assertEqual(self.strand_analyses[0].get_taxonomy(), self.tax)

    def test_get_author(self):
        self.assertEqual(self.strand_analyses[0].get_author(), self.author)

    def test_get_num_learning_outcomes(self):
        self.assertEqual(self.strand_analyses[0].get_num_learning_outcomes(), 23)

    def test_initialse_strand_category_hit_counts_created(self):
        self.strand_analyses[0].initialise_strand_category_hit_counts()
        num_cat_hit_counts = StrandCategoryHitCount.objects.filter(strand_analysis=self.strand_analyses[0]).count()
        self.assertEqual(num_cat_hit_counts, 6)


    def test_learning_outcome_category_hit_count_analyses(self):
        target_hit_counts = [13, 10, 21, 7, 4, 6] # The total number of verb hits for each category
        total_hit_counts = []
        self.strand_analyses[0].learning_outcome_category_hit_count_analyses()
        for category in self.verb_cats:
            los_category_hit_counts = LearningOutcomeCategoryHitCount.objects.filter(category=category.title).all()
            total_hit_counts.append(sum(lo_cat_hit_count.hit_count for lo_cat_hit_count in los_category_hit_counts))
        self.assertEqual(total_hit_counts, target_hit_counts)

    def test_strand_category_hit_count_analysis(self):
        target_hit_counts = [11, 9, 13, 7, 3, 6] # The total number of LOs hitting each category
        self.strand_analyses[0].learning_outcome_category_hit_count_analyses()
        self.strand_analyses[0].strand_category_hit_count_analysis()
        total_hit_counts = [StrandCategoryHitCount.objects.filter(strand_analysis=self.strand_analyses[0]).get(category=category.title).hit_count for category in self.verb_cats]
        self.assertEqual(total_hit_counts, target_hit_counts)

    def test_delete_strand_category_diversities_created(self):
        StrandCategoryDiversity.objects.create(strand_analysis=self.strand_analyses[0])
        self.strand_analyses[0].delete_strand_category_diversities()
        num_cat_diversities = StrandCategoryDiversity.objects.filter(strand_analysis=self.strand_analyses[0]).count()
        self.assertEqual(num_cat_diversities, 0)

    def test_strand_category_diversity_analysis(self):
        target_hit_counts = [6, 11, 3, 3, 0, 0] # The target number of LOs hitting 1, 2, ..., 6 categories
        self.strand_analyses[0].learning_outcome_category_hit_count_analyses()
        self.strand_analyses[0].strand_category_diversity_analysis()
        estimated_hit_counts =[cat_diversity.num_learning_outcomes for cat_diversity in StrandCategoryDiversity.objects.filter(strand_analysis=self.strand_analyses[0]).all()]
        self.assertEqual(estimated_hit_counts, target_hit_counts)

    def test_strand_average_analysis(self):
        self.strand_analyses[0].learning_outcome_category_hit_count_analyses()
        self.strand_analyses[0].strand_category_diversity_analysis()
        self.strand_analyses[0].strand_average_analysis()
        strand_average = StrandAverage.objects.get(strand_analysis=self.strand_analyses[0])
        self.assertEqual(strand_average.verbs, 2.65)
        self.assertEqual(strand_average.categories, 2.13)

    def test_get_category_hit_counts(self):
        target_hit_counts = {'knowledge': 11, 'comprehension': 9, 'application': 13, 'analysis': 7, 'synthesis': 3, 'evaluation': 6}
        self.strand_analyses[0].learning_outcome_category_hit_count_analyses()
        self.strand_analyses[0].strand_category_hit_count_analysis()
        estimated_hit_counts = self.strand_analyses[0].get_category_hit_counts()
        self.assertEqual(estimated_hit_counts, target_hit_counts)

    def test_get_category_diversities(self):
        target_diversities = {1: 6, 2: 11, 3: 3, 4: 3, 5: 0, 6: 0} # Target number of LOs hitting 1, 2.., n categories, as a dictionary
        self.strand_analyses[0].learning_outcome_category_hit_count_analyses()
        self.strand_analyses[0].strand_category_diversity_analysis()
        estimated_diversities = self.strand_analyses[0].get_category_diversities()
        self.assertEqual(estimated_diversities, target_diversities)

    def test_get_verb_average(self):
        target_average = {self.strand_analyses[0].title: 2.65}
        self.strand_analyses[0].learning_outcome_category_hit_count_analyses()
        self.strand_analyses[0].strand_average_analysis()
        estimated_average = self.strand_analyses[0].get_verb_average()
        self.assertEqual(estimated_average, target_average)

    def test_get_category_average(self):
        target_average = {self.strand_analyses[0].title: 2.13}
        self.strand_analyses[0].learning_outcome_category_hit_count_analyses()
        self.strand_analyses[0].strand_category_diversity_analysis()
        self.strand_analyses[0].strand_average_analysis()
        estimated_average = self.strand_analyses[0].get_category_average()
        self.assertEqual(estimated_average, target_average)


class TestLearningOutcomeAnalysis(SetUp):

    def test_str(self):
        lo = self.strands[0].learning_outcomes.first()
        lo_analysis = LearningOutcomeAnalysis.objects.create(strand_analysis=self.strand_analyses[0], learning_outcome=lo)
        self.assertEqual(str(lo_analysis), lo_analysis.slug)

    def test_get_learning_outcome(self):
        lo = self.strands[0].learning_outcomes.first()
        lo_analysis = LearningOutcomeAnalysis.objects.create(strand_analysis=self.strand_analyses[0], learning_outcome=lo)
        self.assertEqual(lo_analysis.get_learning_outcome(), lo)

    def test_get_learning_outcome_text(self):
        lo = self.strands[0].learning_outcomes.first()
        lo_analysis = LearningOutcomeAnalysis.objects.create(strand_analysis=self.strand_analyses[0], learning_outcome=lo)
        self.assertEqual(lo_analysis.get_learning_outcome_text(), lo.text)

    def test_get_learning_outcome_index(self):
        lo = self.strands[0].learning_outcomes.first()
        lo_analysis = LearningOutcomeAnalysis.objects.create(strand_analysis=self.strand_analyses[0], learning_outcome=lo)
        self.assertEqual(lo_analysis.get_learning_outcome_index(), lo.index)

    def test_get_learning_outcome_pk(self):
        lo = self.strands[0].learning_outcomes.first()
        lo_analysis = LearningOutcomeAnalysis.objects.create(strand_analysis=self.strand_analyses[0], learning_outcome=lo)
        self.assertEqual(lo_analysis.get_learning_outcome_pk(), lo.pk)

    def test_get_curriculum(self):
        lo = self.strands[0].learning_outcomes.first()
        lo_analysis = LearningOutcomeAnalysis.objects.create(strand_analysis=self.strand_analyses[0], learning_outcome=lo)
        self.assertEqual(lo_analysis.get_curriculum(), self.curr)

    def test_get_author(self):
        lo = self.strands[0].learning_outcomes.first()
        lo_analysis = LearningOutcomeAnalysis.objects.create(strand_analysis=self.strand_analyses[0], learning_outcome=lo)
        self.assertEqual(lo_analysis.get_author(), self.author)

    def test_get_taxonomy(self):
        lo = self.strands[0].learning_outcomes.first()
        lo_analysis = LearningOutcomeAnalysis.objects.create(strand_analysis=self.strand_analyses[0], learning_outcome=lo)
        self.assertEqual(lo_analysis.get_taxonomy(), self.tax)

    def test_initialse_category_hit_counts_created(self):
        lo = self.strands[0].learning_outcomes.first()
        lo_analysis = LearningOutcomeAnalysis.objects.create(strand_analysis=self.strand_analyses[0], learning_outcome=lo)
        lo_analysis.initialise_category_hit_counts()
        num_cat_hit_counts = LearningOutcomeCategoryHitCount.objects.filter(learning_outcome_analysis=lo_analysis).count()
        self.assertEqual(num_cat_hit_counts, 6)

    def test_hit_count_analysis(self):
        target_hit_count = [1, 1, 1, 0, 1, 0] # The target number of verb hits for the LO across the 6 categories
        lo = self.strands[0].learning_outcomes.first()
        lo_analysis = LearningOutcomeAnalysis.objects.create(strand_analysis=self.strand_analyses[0], learning_outcome=lo)
        lo_analysis.hit_count_analysis()
        lo_cat_hits = LearningOutcomeCategoryHitCount.objects.filter(learning_outcome_analysis=lo_analysis).all()
        estimated_hit_count = [lo_cat_hits.get(category=category.title).hit_count for category in self.verb_cats]
        self.assertEqual(estimated_hit_count, target_hit_count)
