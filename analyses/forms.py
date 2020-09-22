from django. forms import ModelForm

from taxonomies.models import CustomUserTaxonomy as Taxonomy
from .models import CurriculumAnalysis

LABELS = {
        "taxonomy": "Taxonomy* \
                <span class='text-muted'><small>(Choose a taxonomy for the analysis)</small></span>",
                }


class CurriculumAnalysisFormMixin:
    """ A mixin for the curriculum analysis forms """

    def initialise(self, FormClass, *args, **kwargs):
        """ Overriding a forms' __init__ method to filter taxonomy choices appropriately.
        This is achieved by passing the request from the views' get_form_kwargs method """

        request = kwargs.pop('request', None)
        super(FormClass, self).__init__(*args, **kwargs)
        self.fields.get('taxonomy', None).queryset = Taxonomy.objects.filter(author__is_staff=True) \
                | Taxonomy.objects.filter(author=request.user)


class CurriculumAnalysisCreateForm(CurriculumAnalysisFormMixin, ModelForm):


    class Meta:
        model = CurriculumAnalysis
        fields = ['taxonomy']
        labels = LABELS

    def __init__(self, *args, **kwargs):
        self.initialise(CurriculumAnalysisCreateForm, *args, **kwargs)

class CurriculumAnalysisUpdateForm(CurriculumAnalysisFormMixin, ModelForm):


    class Meta:
        model = CurriculumAnalysis
        fields = ['taxonomy']
        labels = LABELS

    def __init__(self, *args, **kwargs):
        self.initialise(CurriculumAnalysisUpdateForm, *args, **kwargs)
