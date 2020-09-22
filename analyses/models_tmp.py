from django.urls import reverse
from django.shortcuts import get_object_or_404

from utils.slugs import unique_slugify
from utils.get import AnalysisGetMethods

from django.db import models

from curricula.models import Curriculum
from strands.models import Strand
from learning_outcomes.models import LearningOutcome
from taxonomies.models import CustomUserTaxonomy as Taxonomy
from verbs.models import Verb

import spacy
import time
import concurrent.futures

nlp = spacy.load('en_core_web_sm')

# The following models are defined in order to separate a curriculum from its' analysis.
# For instance, this allows for a curriculum to have multiple analyses within different taxonomies,
# without changing the properties of the curriculum.

class CurriculumAnalysis(models.Model, AnalysisGetMethods):
    """

    A class to manage the analysis of a curriculum within a given taxonomy

    """
    title = models.CharField(max_length=250)
    date_created = models.DateTimeField(auto_now_add=True)
    curriculum = models.ForeignKey(Curriculum, on_delete=models.CASCADE, related_name='curriculum_analyses')
    taxonomy = models.ForeignKey(Taxonomy, on_delete=models.CASCADE, related_name='curriculum_analyses')
    slug = models.SlugField(max_length=250, blank=True, unique=True)


    class Meta:
        verbose_name = 'Curriculum Analysis'
        verbose_name_plural = 'Curriculum Analyses'


    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('curricula:analyses:detail', kwargs={'pk_curriculum': self.get_curriculum_pk(), 'slug_curriculum': self.get_curriculum_slug(), 'slug_curriculum_analysis': self.slug})

    def save(self, *args, **kwargs):
        slug_str = f"{self.title}"
        unique_slugify(self, slug_str)
        super(CurriculumAnalysis, self).save(*args, **kwargs)
        # a post_save signal is sent to trigger all analyses

    def get_curriculum(self):
        """ Returns the curriculum of the analysis """
        return self.curriculum

    def get_taxonomy(self):
        """ Returns the taxonomy of the analysis """
        return self.taxonomy

    def get_author(self):
        """ Returns the author of the analysis """
        return self.get_curriculum().author

    def get_num_learning_outcomes(self):
        """ Returns the number of learning outcomes in the curriculum """
        return self.curriculum.get_num_learning_outcomes()


    def hit_count_analysis(self):
        """ Generates all the LearningOutcomeCategoryHitCount objects for the
        analysis of the curriculum within the taxonomy. These are the central
        objects from which all other analyses are derived """
        for strand in self.curriculum.strands.all():
            strand_analysis = StrandAnalysis.objects.create(title=f"{self.title}-{strand.title}", curriculum_analysis=self, strand=strand)
            strand_analysis.hit_count_analysis()

    def category_occurrence_analysis(self):
        """ Generates all the StrandCategoryOccurrence objects for the
        analysis of the curriculum within the taxonomy . """
        for strand_analysis in self.strand_analyses.all():
            strand_analysis.category_occurrence_analysis()

    def category_diversity_analysis(self):
        """ Generates all the StrandCategoryDiversity objects for the
        analysis of the curriculum within the taxonomy . """
        for strand_analysis in self.strand_analyses.all():
            strand_analysis.category_diversity_analysis()

    def verb_average_analysis(self):
        """ Generates all the StrandVerbAverage objects for the
        analysis of the curriculum within the taxonomy . """
        for strand_analysis in self.strand_analyses.all():
            strand_analysis.verb_average_analysis()

    def category_diversity_average_analysis(self):
        """ Generates all the StrandCategoryDiversityAverage objects for the
        analysis of the curriculum within the taxonomy . """
        for strand_analysis in self.strand_analyses.all():
            strand_analysis.category_diversity_average_analysis()

    def get_category_occurrences(self):
        """ Returns a list of dictionaries, one for each strand, whose keys are the verb category names
        and values are the number of occurrences of that category in the learning outcomes of the strand"""
        return [strand_analysis.get_category_occurrences() for strand_analysis in self.strand_analyses.all()]

    def get_category_diversities(self):
        """ Returns a list of dictionaries, one for each strand. The dictionaries give the number of LOs
        in 1 category, in 2 categories, ..., n categories (mutually exclusive). Keys are number of
        categories and values are number of LOs """
        return [strand_analysis.get_category_diversities() for strand_analysis in self.strand_analyses.all()]

    def get_verb_averages(self):
        """ Return a list of dictionaries, one for each strand. The dictionaries give the average number
        of verbs per LO in each strand """
        return [strand_analysis.get_verb_average() for strand_analysis in self.strand_analyses.all()]

    def get_category_averages(self):
        """ Return a list of dictionaries, one for each strand. The dictionaries give the average number
        of categories per LO in each strand """
        return [strand_analysis.get_category_diversity_average() for strand_analysis in self.strand_analyses.all()]

class StrandAnalysis(models.Model, AnalysisGetMethods):
    """

    A class to manage the analysis of a curriculums' strand within a given taxonomy

    """
    title = models.CharField(max_length=250)
    date_created = models.DateTimeField(auto_now_add=True)
    curriculum_analysis = models.ForeignKey(CurriculumAnalysis, on_delete=models.CASCADE, related_name='strand_analyses')
    strand = models.ForeignKey(Strand, on_delete=models.CASCADE, related_name='strand_analyses')
    slug = models.SlugField(max_length=250, blank=True, unique=True)


    class Meta:
        verbose_name = 'Strand Analysis'
        verbose_name_plural = 'Strand Analyses'


    def __str__(self):
        return self.title

    def get_absolute_url(self):
        pass

    def save(self, *args, **kwargs):
        slug_str = f"{self.title}"
        unique_slugify(self, slug_str)
        super(StrandAnalysis, self).save(*args, **kwargs)

    def get_curriculum(self):
        """ Return the title of the curriculum of the analysis """
        return self.curriculum_analysis.curriculum

    def get_author(self):
        """ Returns the author of the analysis """
        return self.get_curriculum().author

    def get_taxonomy(self):
        """ Return the taxonomy of the analysis """
        return self.curriculum_analysis.taxonomy

    def get_num_learning_outcomes(self):
        """ Returns the number of learning outcomes in the strand """
        return self.strand.get_num_learning_outcomes()

    def hit_count_analysis(self):
        for learning_outcome in self.strand.learning_outcomes.all():
            learning_outcome_analysis = LearningOutcomeAnalysis.objects.create(index=learning_outcome.index, strand_analysis=self, learning_outcome=learning_outcome)
            learning_outcome_analysis.hit_count_analysis()

    def category_occurrence_analysis(self):
        """ Calculates the number of LOs in each category
        """
        categories = self.get_taxonomy().verb_categories.all()
        lo_analyses = self.learning_outcome_analyses.all()
        category_occurrences = [0 for _ in categories] # Number of LOs in each category
        for lo_analysis in lo_analyses:
            hit_counts = lo_analysis.learning_outcome_category_hit_counts.all()
            for cat_index, hit_count in enumerate(hit_counts):
                if hit_count.frequency_count > 0:
                    category_occurrences[cat_index] += 1
        # Create object in the database
        self.create_category_occurrence(category_occurrences)

    def create_category_occurrence(self, category_occurrences):
        """ Creates a new StrandCategoryOccurrence object in the database from the category_occurrences
        generated in the category_occurrence_analysis method """

        categories = self.get_taxonomy().verb_categories.all()
        for category, occurrence in zip(categories, category_occurrences):
            strand_category_occurrence = StrandCategoryOccurrence.objects.create(category=category.title, strand_analysis=self)
            strand_category_occurrence.occurrences = occurrence
            strand_category_occurrence.save()

    def category_diversity_analysis(self):
        """ Calculates the number of LOs hitting 1, 2, 3 ..., n categories (mutually exclusive)
        """
        lo_analyses = self.learning_outcome_analyses.all()
        category_diversities = [0 for _ in lo_analyses]   # List of category numbers reached by each LO in the strand
        for lo_index, lo_analysis in enumerate(lo_analyses):
            for hit_count in lo_analysis.learning_outcome_category_hit_counts.all():
                if hit_count.frequency_count > 0:
                    category_diversities[lo_index] += 1
        # Create object in the database
        self.create_category_diversity(category_diversities)

    def create_category_diversity(self, category_diversities):
        """ Creates a new StrandCategorydiversity object in the database from the category_diversities
        generated in the category_diversity_analysis method """

        total_num_categories = self.get_taxonomy().verb_categories.count()
        for category_num_to_check in range(1, total_num_categories + 1):
            strand_category_diversity = StrandCategoryDiversity.objects.create(strand_analysis=self, num_categories=category_num_to_check)
            strand_category_diversity.num_learning_outcomes = category_diversities.count(category_num_to_check)
            strand_category_diversity.save()

    def verb_average_analysis(self):
        """ Calculates the average number of verbs per LO in the strand """
        total_verb_hits = 0
        total_los = self.get_num_learning_outcomes()
        lo_analyses = self.learning_outcome_analyses.all()
        for lo_analysis in lo_analyses:
            hit_counts = lo_analysis.learning_outcome_category_hit_counts.all()
            total_verb_hits += sum(hit_count.frequency_count for hit_count in hit_counts)
        average = total_verb_hits / total_los
        self.create_verb_average(average)

    def create_verb_average(self, average):
        """ Creates a new StrandVerbAverage object in the database from the average generated
        in the verb_average_analysis method """
        strand_verb_average = StrandVerbAverage.objects.create(strand_analysis=self, verb_average=average)
        strand_verb_average.save()

    def category_diversity_average_analysis(self):
        """ Calculates the average number of verb categories per LO, must be run after
        the category_diversity_analysis method """
        diversities = self.get_category_diversities()
        total_los = self.get_num_learning_outcomes()
        total_category_hits = sum(num_cats * num_los for num_cats, num_los in zip(diversities.keys(), diversities.values()))
        average = total_category_hits / total_los
        self.create_category_diversity_average(average)

    def create_category_diversity_average(self, average):
        """ Creates a new StrandCategoryDiversityAverage object in the database from the average generated
        in the category_diversity_average_analysis method """
        strand_cat_diversity_average = StrandCategoryDiversityAverage.objects.create(strand_analysis=self, category_average=average)
        strand_cat_diversity_average.save()


    def get_category_occurrences(self):
        """ Return a dictionary whose keys are the verb category names and values are the
        number of occurrences of that category in the learning outcomes of the strand"""
        return {strand_cat_occurrence.category: strand_cat_occurrence.occurrences for strand_cat_occurrence in self.strand_category_occurrences.all()}

    def get_category_diversities(self):
        """ Returns the number of LOs hitting 1 category, 2 categories etc.. """

        return {strand_cat_diversity.num_categories: strand_cat_diversity.num_learning_outcomes for strand_cat_diversity in self.strand_category_diversities.all()}

    def get_verb_average(self):
        """ Returns the average number of verbs per LO in the strand """

        return {self.strand.title: self.strand_verb_averages.all().first().verb_average}

    def get_category_diversity_average(self):
        """ Returns the average number of categories per LO in the strand"""

        return {self.strand.title: self.strand_category_diversity_averages.all().first().category_average}


class LearningOutcomeAnalysis(models.Model, AnalysisGetMethods):
    """

    A class to manage the analysis of a learning outcome of a curriculums' strand, within a given taxonomy

    """
    index = models.PositiveIntegerField(default=0)
    date_created = models.DateTimeField(auto_now_add=True)
    strand_analysis = models.ForeignKey(StrandAnalysis, on_delete=models.CASCADE, related_name='learning_outcome_analyses')
    learning_outcome = models.ForeignKey(LearningOutcome, on_delete=models.CASCADE, related_name='learning_outcome_analyses')
    slug = models.SlugField(max_length=250, blank=True, unique=True)


    class Meta:
        verbose_name = 'Learning Outcome Analysis'
        verbose_name_plural = 'Learning Outcome Analyses'


    def __str__(self):
        return self.slug

    def get_absolute_url(self):
        pass

    def save(self, *args, **kwargs):
        slug_str = f"{self.get_strand_title()} {self.index}"
        unique_slugify(self, slug_str)
        super(LearningOutcomeAnalysis, self).save(*args, **kwargs)

    def get_learning_outcome(self):
        """ Returns the learning outcome of the LO-analysis """
        return self.learning_outcome

    def get_learning_outcome_text(self):
        """ Returns the text of the learning outcome of the LO-analysis """
        return self.get_learning_outcome().text

    def get_learning_outcome_index(self):
        """ Returns the index of the LO withing the strand """
        return self.get_learning_outcome().index

    def get_learning_outcome_pk(self):
        """ Returns the primary key of the LO """
        return self.get_learning_outcome().pk

    def get_strand_pk(self):
        """ Returns the primary key of the strand of the LO/analysis """
        return self.get_strand().pk

    def get_strand_slug(self):
        """ Returns the slug of the strand of the LO/analysis """
        return self.get_strand().slug

    def get_strand(self):
        """ Returns the strand of the LO/analysis """
        return self.learning_outcome.strand

    def get_strand_title(self):
        """ Returns the title of the strand of the LO/analysis """
        return self.get_strand().title

    def get_strand_pk(self):
        """ Returns the primary key of the strand of the LO/analysis """
        return self.get_strand().pk

    def get_strand_slug(self):
        """ Returns the slug of the strand of the LO/analysis """
        return self.get_strand().slug

    def get_curriculum(self):
        """ Returns the curriculum of the LO """
        return self.strand_analysis.curriculum_analysis.curriculum

    def get_author(self):
        """ Returns the author of the analysis """
        return self.strand_analysis.curriculum_analysis.curriculum.author

    def get_taxonomy(self):
        return self.strand_analysis.curriculum_analysis.taxonomy

    def hit_count_analysis(self):
        self.initialise_learning_outcome_category_hits()
        allowed_non_verbs = ["who", "what", "where", "when", "why"]
        non_detected_verbs = []
        tokenised_LO = nlp(self.learning_outcome.text)
        for token in tokenised_LO:
            if (token.pos_ == "VERB" or token.text in (allowed_non_verbs or non_detected_verbs)):
                verb = Verb.objects.filter(title=token.lemma_).first()
                if verb:
                    target_verb_categories = verb.verb_categories.filter(taxonomy=self.get_taxonomy())
                    for verb_category in target_verb_categories.all():
                        target = self.learning_outcome_category_hit_counts.get(category=verb_category.title)
                        target.frequency_count += 1
                        target.save()

    def initialise_learning_outcome_category_hits(self):
        target_taxonomy = self.get_taxonomy()
        for verb_category in target_taxonomy.verb_categories.all():
            LearningOutcomeCategoryHitCount.objects.create(category=verb_category.title, learning_outcome_analysis=self)


class LearningOutcomeCategoryHitCount(models.Model):
    """

    A class to manage the verb category hit count of a learning outcome within a given taxonomy.
    A LearningOutcomeAnalysis instance has a collection of LearningOutcomeCategoryHitCount instances,
    where each instance stores the number of verbs appearing in a learning outcome
    from a given verb category of the taxonomy. Each instance pertains to a specific learning outcome
    and verb category. E.g. for 6 verb categories, 3 curriculum strands with 22, 15 and 18
        learning outcomes, then 6*(22+15+18) objects are created.
    fields: - category: should be the verb category title of the taxonomy
            - frequency_count: represents the number of verb hits in the learning outcome

    """

    category = models.CharField(max_length=150)
    frequency_count = models.PositiveIntegerField(default=0)
    learning_outcome_analysis = models.ForeignKey(LearningOutcomeAnalysis, on_delete=models.CASCADE, related_name='learning_outcome_category_hit_counts')


class StrandCategoryOccurrence(models.Model):
    """

    A class to manage the occurrences of verb categories within a given
    strand. When at least 1 verb from a given category appears in a
    strands' LO, the LO contributes to an additional occurrence of the
    verb category in the strand.
    fields: - category: should be the verb category title of the taxonomy
            - occurrences: represents the number of learning outcomes in
            the strand which hit/reach the given verb category

    """
    category = models.CharField(max_length=150)
    occurrences = models.PositiveIntegerField(default=0)
    strand_analysis = models.ForeignKey(StrandAnalysis, on_delete=models.CASCADE, related_name='strand_category_occurrences')


class StrandCategoryDiversity(models.Model):
    """

    A class to manage the category diversity of learning outcomes in a curriculum, e.g.
    the number of LOs appearing in 1 verb category, 2 verb categories ... (mutually exclusive)
    fields: - num_categories: a common number of categories that a collection of LOs share
            - num_of_LOs: The number of LOs in the collection sharing a common number of categories

    """
    num_categories = models.PositiveIntegerField(default=0)
    num_learning_outcomes = models.PositiveIntegerField(default=0)
    strand_analysis = models.ForeignKey(StrandAnalysis, on_delete=models.CASCADE, related_name='strand_category_diversities')


class StrandCategoryDiversityAverage(models.Model):
    """
    A class to represent the average number of categories in each learning outcome
    """

    category_average = models.FloatField(default=0)
    strand_analysis = models.ForeignKey(StrandAnalysis, on_delete=models.CASCADE, related_name='strand_category_diversity_averages')


class StrandVerbAverage(models.Model):
    """
    A class to represent the average number of verbs per learning outcome in a strand.
    """

    verb_average = models.FloatField(default=0)
    strand_analysis = models.ForeignKey(StrandAnalysis, on_delete=models.CASCADE, related_name='strand_verb_averages')


