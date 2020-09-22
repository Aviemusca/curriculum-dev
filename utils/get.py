""" All classes here are meant to be inhereted by other classes for their methods """
class AnalysisGetMethods:
    pass

class CurriculumGetMethods:
    """ Classes using these methods should have an appropriately defined get_curriculum method. """

    def get_curriculum_pk(self):
        """ Returns the primary key of the curriculum """
        return self.get_curriculum().pk

    def get_curriculum_title(self):
        """ Return the title of the curriculum """
        return self.get_curriculum().title

    def get_curriculum_slug(self):
        """ Return the slug of the curriculum of the analysis """
        return self.get_curriculum().slug


class AuthorGetMethods:
    """ Classes using these methods should have an appropriately defined get_author method. """

    def get_author_username(self):
        """ Returns the username of the author of the analysis """
        return self.get_author().username

    def get_author_pk(self):
        """ Returns the primary key of the author of the analysis """
        return self.get_author().pk

class TaxonomyGetMethods:
    """ Classes using these methods should have an appropriately defined get_taxonomy method. """

    def get_taxonomy_title(self):
        """ Return the title of the taxonomy of the analysis """
        return self.get_taxonomy().title

    def get_taxonomy_pk(self):
        """ Return the primary key of the taxonomy of the analysis """
        return self.get_taxonomy().pk

    def get_taxonomy_slug(self):
        """ Return the slug of the taxonomy of the analysis """
        return self.get_taxonomy().slug

class StrandGetMethods:
    """ Classes using these methods should have an appropriately defined get_strand method. """

    def get_strand_title(self):
        """ Returns the title of the strand of the LO/analysis """
        return self.get_strand().title

    def get_strand_pk(self):
        """ Returns the primary key of the strand of the LO/analysis """
        return self.get_strand().pk

    def get_strand_slug(self):
        """ Returns the slug of the strand of the LO/analysis """
        return self.get_strand().slug


class LearningOutcomeGetMethods:
    """ Classes using these methods should have an appropriately defined get_learning_outcome method. """

    def get_learning_outcome_text(self):
        """ Returns the text of the learning outcome of the LO-analysis """
        return self.get_learning_outcome().text

    def get_learning_outcome_index(self):
        """ Returns the index of the LO withing the strand """
        return self.get_learning_outcome().index

    def get_learning_outcome_pk(self):
        """ Returns the primary key of the LO """
        return self.get_learning_outcome().pk

class CurriculumAnalysisGetMethods(
        CurriculumGetMethods,
        AuthorGetMethods,
        TaxonomyGetMethods
        ):
    pass


class StrandAnalysisGetMethods(
        CurriculumGetMethods,
        AuthorGetMethods,
        TaxonomyGetMethods
        ):
    pass


class LearningOutcomeAnalysisGetMethods(
        CurriculumGetMethods,
        AuthorGetMethods,
        TaxonomyGetMethods,
        StrandGetMethods,
        LearningOutcomeGetMethods
        ):
    pass

class VerbCategoryMixin(
        TaxonomyGetMethods,
        AuthorGetMethods,
        ):
    pass
