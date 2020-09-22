from django.urls import reverse
from django.shortcuts import get_object_or_404

from utils.slugs import unique_slugify
from utils.get import (
        CurriculumAnalysisGetMethods,
        StrandAnalysisGetMethods,
        LearningOutcomeAnalysisGetMethods,
        )

from django.db import models

from curricula.models import Curriculum
from strands.models import Strand
from learning_outcomes.models import LearningOutcome
from taxonomies.models import CustomUserTaxonomy as Taxonomy
from verbs.models import Verb, NonVerb, NonCatVerb

import spacy

nlp = spacy.load('en_core_web_sm')

# The following models are defined in order to separate a curriculum from its' analysis.
# For instance, this allows for a curriculum to have multiple analyses within different taxonomies,
# without changing the properties of the curriculum.

class CurriculumAnalysis(models.Model, CurriculumAnalysisGetMethods):
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
        slug_str = f"analysis-{self.taxonomy}"
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

    def get_non_cat_verbs(self):
        """ Returns the non categorised verbs of the analysis as a string """
        return ", ".join([verb.title for verb in self.non_cat_verbs.all()])

    def get_num_non_cat_verbs(self):
        """ Returns the number of non categorised verbs in the analysis """
        return self.non_cat_verbs.all().count()

    def has_non_cat_verb(self):
        """ Returns True if at least 1 categorised verb in the analysis """
        return self.non_cat_verbs.all().count() > 0

    def initialise(self):
        """  Initialisation called for every new analysis """
        self.initialise_non_cat_verbs()
        strand_analyses = self.initialise_strand_analyses()
        return strand_analyses

    def initialise_non_cat_verbs(self):
        """  Removes any previous non-categorised verbs from the curriculum analysis """
        non_cat_verbs = NonCatVerb.objects.filter(curriculum_analyses__pk=self.pk)
        for non_cat_verb in non_cat_verbs:
            non_cat_verb.curriculum_analyses.remove(self)
            if non_cat_verb.curriculum_analyses.count() == 0:
                non_cat_verb.delete()

    def initialise_strand_analyses(self):
        """ Deletes any pre-existing strand anlyses and returns a fresh collection """
        StrandAnalysis.objects.filter(curriculum_analysis=self).delete()
        return [StrandAnalysis.objects.create(title=f"{self.title}-{strand.title}", curriculum_analysis=self, strand=strand) for strand in self.curriculum.strands.all()]

    def learning_outcome_category_hit_count_analyses(self):
        """ Generates all the LearningOutcomeCategoryHitCount objects for the
        analysis of the curriculum within the taxonomy (over all strands). These are the central
        objects from which all other analyses are derived """
        StrandAnalysis.objects.filter(curriculum_analysis=self).delete()
        for strand in self.curriculum.strands.all():
            strand_analysis = StrandAnalysis.objects.create(title=f"{self.title}-{strand.title}", curriculum_analysis=self, strand=strand)
            strand_analysis.learning_outcome_category_hit_count_analyses()

    def strand_category_hit_count_analyses(self):
        """ Generates all the StrandCategoryHitCount objects for the
        analysis of the curriculum within the taxonomy . """
        for strand_analysis in self.strand_analyses.all():
            strand_analysis.strand_category_hit_count_analysis()

    def strand_category_diversity_analyses(self):
        """ Generates all the StrandCategoryDiversity objects for the
        analysis of the curriculum within the taxonomy . """
        for strand_analysis in self.strand_analyses.all():
            strand_analysis.strand_category_diversity_analysis()

    def strand_average_analyses(self):
        """ Generates all the StrandAverage objects for the
        analysis of the curriculum within the taxonomy . """
        for strand_analysis in self.strand_analyses.all():
            strand_analysis.strand_average_analysis()

    def get_category_hit_counts(self):
        """ Returns a list of dictionaries, one for each strand, whose keys are the verb category names
        and values are the number of occurrences of that category in the learning outcomes of the strand"""
        return [strand_analysis.get_category_hit_counts() for strand_analysis in self.strand_analyses.all()]

    def get_category_diversities(self):
        """ Returns a list of dictionaries, one for each strand. The dictionaries give the number of LOs
        in 1 category, in 2 categories, ..., n categories (mutually exclusive). Keys are number of
        categories and values are number of LOs """
        return [strand_analysis.get_category_diversities() for strand_analysis in self.strand_analyses.all()]

    def get_strand_colours(self):
        """ Returns a list of colours for each strand """
        return [strand_analysis.strand.colour for strand_analysis in self.strand_analyses.all()]

    def get_verb_averages(self):
        """ Return a list of dictionaries, one for each strand. The dictionaries give the average number
        of verbs per LO in each strand """
        return [strand_analysis.get_verb_average() for strand_analysis in self.strand_analyses.all()]

    def get_category_averages(self):
        """ Return a list of dictionaries, one for each strand. The dictionaries give the average number
        of categories per LO in each strand """
        return [strand_analysis.get_category_average() for strand_analysis in self.strand_analyses.all()]


class StrandAnalysis(models.Model, StrandAnalysisGetMethods):
    """

    A class to manage the analysis of a curriculums' strand/module within a given taxonomy

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

    def initialise_learning_outcome_analyses(self):
        """ Deletes any pre-existing learning outcome anlyses and returns a fresh collection """
        LearningOutcomeAnalysis.objects.filter(strand_analysis=self).delete()
        return [LearningOutcomeAnalysis.objects.create(index=lo.index, strand_analysis=self, learning_outcome=lo) for lo in self.strand.learning_outcomes.all()]

    def learning_outcome_category_hit_count_analyses(self):
        """ Calculates how many times each category appears in a given LO, for all LOs in the strand """
        los = self.strand.learning_outcomes.all()
        for lo in los:
            lo_analysis = LearningOutcomeAnalysis.objects.create(index=lo.index, strand_analysis=self, learning_outcome=lo)
            lo_analysis.hit_count_analysis()

    def initialise_strand_category_hit_counts(self):
        """ Deletes any pre-existing category_hit_count objects and returns a fresh collection """
        self.strand_category_hit_counts.all().delete()
        categories = self.get_taxonomy().verb_categories.all()
        return [StrandCategoryHitCount.objects.create(category=category.title, strand_analysis=self) for category in categories]

    def strand_category_hit_count_analysis(self):
        """ Calculates the number of LOs in each category across the strand """
        strand_cat_hit_counts = self.initialise_strand_category_hit_counts()
        lo_analyses = self.learning_outcome_analyses.all()
        categories = self.get_taxonomy().verb_categories.all()
        for cat_index, category in enumerate(categories):
            for lo_analysis in lo_analyses:
                lo_cat_hit_count = lo_analysis.learning_outcome_category_hit_counts.get(category=category)
                if lo_cat_hit_count.hit_count > 0:
                    strand_cat_hit_counts[cat_index].hit_count += 1
                    strand_cat_hit_counts[cat_index].save()

    def delete_strand_category_diversities(self):
        """ Deletes any pre-existing strand_category_diversity """
        self.strand_category_diversities.all().delete()

    def initialise_strand_category_diversities(self):
        """ Deletes any pre-existing category_diversity objects and returns a fresh collection """
        self.strand_category_diversities.all().delete()
        categories = self.get_taxonomy().verb_categories.all()
        return [StrandCategoryDiversity.objects.create(num_categories=index+1, strand_analysis=self) for index, category in enumerate(categories)]


    def strand_category_diversity_analysis(self):
        """ Calculates the number of LOs hitting 1, 2, 3 ..., n categories (mutually exclusive) """
        self.delete_strand_category_diversities()
        lo_analyses = self.learning_outcome_analyses.all()
        category_diversities = [0 for _ in lo_analyses]   # List of category numbers reached by each LO in the strand
        for lo_index, lo_analysis in enumerate(lo_analyses):
            for cat_hit_count in lo_analysis.learning_outcome_category_hit_counts.all():
                if cat_hit_count.hit_count > 0:
                    category_diversities[lo_index] += 1
        # Create object in the database
        self.create_strand_category_diversity(category_diversities)

    def create_strand_category_diversity(self, category_diversities):
        """ Creates the StrandCategorydiversity objects in the database from the category_diversities
        generated in the category_diversity_analysis method """

        print(category_diversities)
        total_num_categories = self.get_taxonomy().verb_categories.count()
        for category_num_to_check in range(0, total_num_categories + 1):
            strand_category_diversity = StrandCategoryDiversity.objects.create(strand_analysis=self, num_categories=category_num_to_check)
            strand_category_diversity.num_learning_outcomes = category_diversities.count(category_num_to_check)
            strand_category_diversity.save()


    def initialise_strand_average(self):
        """ Deletes any pre-existing strand_verb_average object and creates a fresh one """
        StrandAverage.objects.filter(strand_analysis=self).delete()
        StrandAverage.objects.create(strand_analysis=self)

    def strand_average_analysis(self):
        """ Calcultaes the average properties of the strand across LOs """
        self.initialise_strand_average()
        self.strand_verb_average_analysis()
        self.strand_category_average_analysis()

    def strand_verb_average_analysis(self):
        """ Calculates the average number of verbs per LO in the strand """
        total_verb_hits = 0
        total_los = self.get_num_learning_outcomes()
        lo_analyses = self.learning_outcome_analyses.all()
        for lo_analysis in lo_analyses:
            lo_cat_hit_counts = lo_analysis.learning_outcome_category_hit_counts.all()
            total_verb_hits += sum(cat_hit_count.hit_count for cat_hit_count in lo_cat_hit_counts)
        average = round(total_verb_hits / total_los, 2)
        self.set_verb_average(average)

    def set_verb_average(self, average):
        """ Updates the StrandAverage object in the database with the computed verb average generated
        in the strand_verb_average_analysis method """
        strand_average = StrandAverage.objects.get(strand_analysis=self)
        strand_average.verbs = average
        strand_average.save()

    def strand_category_average_analysis(self):
        """ Calculates the average number of verb categories per LO in the strand.
        Must be run after the category_diversity_analysis method """
        diversities = self.get_category_diversities()
        total_los = self.get_num_learning_outcomes()
        total_category_hits = sum(num_cats * num_los for num_cats, num_los in zip(diversities.keys(), diversities.values()))
        average = round(total_category_hits / total_los, 2)
        self.set_category_average(average)

    def set_category_average(self, average):
        """ Updates the StrandAverage object in the database with the computed category average generated
        in the strand_category_average method """
        strand_average = StrandAverage.objects.get(strand_analysis=self)
        strand_average.categories = average
        strand_average.save()

    def get_category_hit_counts(self):
        """ Return a dictionary whose keys are the verb category names and values are the
        hit counts (number of occurrences) of that category in the learning outcomes of the strand"""
        return {strand_cat_hit_count.category: strand_cat_hit_count.hit_count for strand_cat_hit_count in self.strand_category_hit_counts.all()}

    def get_category_diversities(self):
        """ Returns the number of LOs hitting 1 category, 2 categories etc.. """
        return {strand_cat_diversity.num_categories: strand_cat_diversity.num_learning_outcomes for strand_cat_diversity in self.strand_category_diversities.all()}

    def get_verb_average(self):
        """ Returns the average number of verbs per LO in the strand analysis """
        return {self.title: StrandAverage.objects.get(strand_analysis=self).verbs}

    def get_category_average(self):
        """ Returns the average number of categories per LO in the strand"""
        return {self.title: StrandAverage.objects.get(strand_analysis=self).categories}



class LearningOutcomeAnalysis(models.Model, LearningOutcomeAnalysisGetMethods):
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

    def get_strand(self):
        """ Returns the strand of the LO/analysis """
        return self.learning_outcome.strand

    def get_curriculum(self):
        """ Returns the curriculum of the LO """
        return self.strand_analysis.curriculum_analysis.curriculum

    def get_author(self):
        """ Returns the author of the analysis """
        return self.strand_analysis.curriculum_analysis.curriculum.author

    def get_taxonomy(self):
        """ Returns the taxonomy of the analysis """
        return self.strand_analysis.curriculum_analysis.taxonomy

    #def get_ordered_verb_categories(self):
    #    """ Returns the verb category objects of the taxonomy ordered by level of abstraction """
    #    return VerbCategory.objects.filter(taxonomy=self.get_taxonomy()).order_by('level').all()

    def hit_count_analysis(self):
        """ Initialises a collection of category_hit_count objects for the LO analysis, then
        calculates the number of category hits using the spaCy nlp toolkit """
        self.initialise_category_hit_counts()
        all_allowed_non_verbs = [non_verb.title for non_verb in NonVerb.objects.all()]
        lo_text = self.get_learning_outcome().text
        tokenised_LO = nlp(lo_text)
        for token in tokenised_LO:
            if token.pos_ == "VERB":
                self.handle_detected_verb(token.lemma_)
            elif token.text in all_allowed_non_verbs:
                self.handle_detected_allowed_non_verb(token.text)

    def handle_detected_verb(self, verb_title):
        taxonomy = self.get_taxonomy()
        verb = Verb.objects.filter(title=verb_title).filter(verb_categories__taxonomy=taxonomy).first()
        if verb:
            target_verb_categories = verb.verb_categories.filter(taxonomy=taxonomy)
            for verb_category in target_verb_categories.all():
                target = self.learning_outcome_category_hit_counts.get(category=verb_category.title)
                target.hit_count += 1
                target.save()
        else:
            self.add_verb_to_non_cat_verbs(verb_title)

    def handle_detected_allowed_non_verb(self, non_verb_title):
        taxonomy = self.get_taxonomy()
        non_verb = NonVerb.objects.filter(title=non_verb_title).first()
        if non_verb:
            target_verb_categories = non_verb.verb_categories.filter(taxonomy=taxonomy)
            for verb_category in target_verb_categories.all():
                target = self.learning_outcome_category_hit_counts.get(category=verb_category.title)
                target.hit_count += 1
                target.save()

    def initialise_category_hit_counts(self):
        """ Deletes any pre-existing category_hit_count objects and creates a fresh collection """
        self.learning_outcome_category_hit_counts.all().delete()
        target_taxonomy = self.get_taxonomy()
        for verb_category in target_taxonomy.verb_categories.all():
            LearningOutcomeCategoryHitCount.objects.create(category=verb_category.title, learning_outcome_analysis=self)


    def add_verb_to_non_cat_verbs(self, verb):
        """ Creates a non-categorised verb/ Adds the curriculum analysis
        to a pre-existing non-cat verb """
        curriculum_analysis = self.strand_analysis.curriculum_analysis
        if verb not in [non_cat_verb.title for non_cat_verb in NonCatVerb.objects.all()]:
            non_cat_verb = NonCatVerb.objects.create(title=verb)
        else:
            non_cat_verb = NonCatVerb.objects.filter(title=verb).first()
        non_cat_verb.curriculum_analyses.add(curriculum_analysis)
        non_cat_verb.save()





class LearningOutcomeCategoryHitCount(models.Model):
    """

    A class to represent the verb category hit count of a learning outcome within a given taxonomy.
    A LearningOutcomeAnalysis instance has a collection of LearningOutcomeCategoryHitCount instances,
    one for each category of the taxonomy.
    Each instance pertains to a specific learning outcome and verb category.
    Each instance stores the number of verbs from said category appearing in said learning outcome.
    E.g. for 6 verb categories, 3 curriculum strands with 22, 15 and 18
        learning outcomes, then 6*(22+15+18) objects are created.
    fields: - category : the title of the verb category of a taxonomy
            - hit_count: the number of verb hits from said category in said LO

    """

    category = models.CharField(max_length=150)
    hit_count = models.PositiveIntegerField(default=0)
    learning_outcome_analysis = models.ForeignKey(LearningOutcomeAnalysis, on_delete=models.CASCADE, related_name='learning_outcome_category_hit_counts')


class StrandCategoryHitCount(models.Model):
    """

    A class to represent the verb category hit count of a strand within a given taxonomy.
    A StrandAnalysis instance has a collection of StrandCategoryHitCount instances, one for
    each category of the taxonomy.
    Each instance pertains to a specific strand and verb category.
    Each instance stores the number of appearances of said category in the LOs of said strand.
    A category appears in a strands' LO when the LO contains at least 1 verb from said category.
    A category either appears or not (i.e. does not appear more than once in an LO)
    fields: - category: the title of the verb category of a taxonomy
            - hit_count: the number of appearances of said category in the strand

    """
    category = models.CharField(max_length=150)
    hit_count = models.PositiveIntegerField(default=0)
    strand_analysis = models.ForeignKey(StrandAnalysis, on_delete=models.CASCADE, related_name='strand_category_hit_counts')


class StrandCategoryDiversity(models.Model):
    """

    A class to represent the category diversity of a strand within a given taxonomy.
    A StrandAnalysis instance has a collection of StrandCategoryDiversity instances, one for
    each category collection number of the taxonomy.
    Each instance pertains to a specific strand and verb category number.
    Each instance stores the number of LOs of said strand appearing in said category number.
    e.g. for category num = 3, then -> the number of LOs refers to those appearing simulaneously
    in 3 verb categories (mutually exclusive).
    fields: - num_categories: common number of categories that a collection of LOs share
            - num_learning_outcomes: The number of LOs in the collection sharing a common
            category number

    """
    num_categories = models.PositiveIntegerField(default=0)
    num_learning_outcomes = models.PositiveIntegerField(default=0)
    strand_analysis = models.ForeignKey(StrandAnalysis, on_delete=models.CASCADE, related_name='strand_category_diversities')


class StrandAverage(models.Model):
    """
    A class to represent the average quantities of a strand analysis.
    Averages are taken over the LOs of the strand.
    fields: - categories: average number of categories in each LO
            - verbs: average number of verbs in each LO

    """
    verbs = models.FloatField(default=0)
    categories = models.FloatField(default=0)
    strand_analysis = models.OneToOneField(StrandAnalysis, on_delete=models.CASCADE, related_name='strand_average')
