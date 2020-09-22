from django import forms

from .models import CustomUserTaxonomy

from utils.forms.clean import profanity_clean_fields

LABELS = {
        "title": "Title* \
                <span class='text-muted'><small>(Enter the title of the taxonomy)</small></span>",
                }

WIDGETS = {
        'title': forms.TextInput(attrs={'placeholder': 'e.g. Blooms Modified'}),
        }

class TaxonomyCreateForm(forms.ModelForm):


    class Meta:
        model = CustomUserTaxonomy
        fields = ['title']
        labels = LABELS
        widgets = WIDGETS

    def clean(self):
        cleaned_data = profanity_clean_fields(TaxonomyCreateForm, self)

class TaxonomyUpdateForm(forms.ModelForm):


    class Meta:
        model = CustomUserTaxonomy
        fields = ['title']
        labels = LABELS
        widgets = WIDGETS

    def clean(self):
        cleaned_data = profanity_clean_fields(TaxonomyUpdateForm, self)
