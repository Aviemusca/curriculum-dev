from django import forms
from django.http import Http404

from utils.forms.clean import profanity_clean_field
from .models import VerbCategory
from taxonomies.models import CustomUserTaxonomy as Taxonomy

LABELS = {
        "title": "Title* \
                <span class='text-muted'><small>(Enter the title of the verb category)</small></span>",
        "level": "Level* \
                <span class='text-muted'><small>(Enter the level of the verb category within the taxonomy)</small></span>",
        "verb_list": "Verb List* \
                <span class='text-muted'><small>(Enter all the verbs of the verb category. <strong style='color: crimson;'>Make sure verbs are comma-separated and allowed non-verbs are enclosed in parentheses!)</strong></small></span>",
                }

WIDGETS = {
        'title': forms.TextInput(attrs={'placeholder': 'e.g. Knowledge'}),
        'verb_list': forms.Textarea(attrs={'placeholder': 'e.g. identify, name, recite, state, (who), (what), (where), (when), (why), select, define, describe, label, match, pick, recognise, recognize, list, read, write, outline, retrieve'}),
        }


class VerbCategoryFormMixin:
    """ A mixin for the verb category forms """

    def initialise(self, FormClass, *args, **kwargs):
        """ Overriding a forms' __init__ method to perform validation checks on the
        verb category level within the taxonomy """
        self.taxonomy = kwargs.pop('taxonomy', None)
        # The original/old category, for update view case
        self.old_category = kwargs.pop('category', None)
        super(FormClass, self).__init__(*args, **kwargs)

    def clean_level_(self):
        """ Ensure the user does not input a level value equal to that of a pre-existing
        verb category of the taxonomy """
        try:
            # Get the verb categories of the taxonomy
            verb_cats = VerbCategory.objects.filter(taxonomy=self.taxonomy)
        except Taxonomy.DoesNotExist:
            raise Http404('The taxonomy does not exist!')
        else:

            # Check categories for the entered level value
            submitted_level = self.cleaned_data.get('level', None)

            # if updating, need to allow the original level value to be re-entered
            old_level = None if not self.old_category else self.old_category.level

            if submitted_level in [cat.level for cat in verb_cats.all()\
                    if cat.level != old_level]:
                culprit = verb_cats.get(level=submitted_level)
                raise forms.ValidationError(f'The verb category "{culprit.title}" \
                        already has this value!')

            return submitted_level


class VerbCategoryCreateForm(VerbCategoryFormMixin, forms.ModelForm):


    class Meta:
        model = VerbCategory
        fields = ['title', 'level', 'verb_list',]
        labels = LABELS
        widgets = WIDGETS

    def __init__(self, *args, **kwargs):
        self.initialise(VerbCategoryCreateForm, *args, **kwargs)

    def clean_title(self):
        return profanity_clean_field(self, 'title')

    def clean_level(self):
        return self.clean_level_()


class VerbCategoryUpdateForm(VerbCategoryFormMixin, forms.ModelForm):


    class Meta:
        model = VerbCategory
        fields = ['title', 'level', 'verb_list',]
        labels = LABELS
        widgets = WIDGETS

    def __init__(self, *args, **kwargs):
        self.initialise(VerbCategoryUpdateForm, *args, **kwargs)

    def clean_title(self):
        return profanity_clean_field(self, 'title')

    def clean_level(self):
        return self.clean_level_()
