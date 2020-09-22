from django import forms

from .models import Strand

from utils.forms.clean import profanity_clean_field


LABELS = {
        "title": "Title* \
                <span class='text-muted'><small>(Enter the title of the module)</small></span>",
        "colour": "Colour \
                <span class='text-muted'><small>(Choose the colour of the module in charts)</small></span>",
        "learning_outcome_list": "Learning Outcome list* \
                <span class='text-muted'><small>(Enter all the learning outcomes of the module. <strong style='color: crimson;'>Make sure each learning outcome is on a separate line!)</strong></small></span>",
                }

WIDGETS = {
        'title': forms.TextInput(attrs={'placeholder': 'e.g. Core Concepts'}),
        'colour': forms.TextInput(attrs={'type': 'color'}),
        'learning_outcome_list': forms.Textarea(attrs={'placeholder': f'e.g. Students should be able to critically examine ...\nStudents should be able to evaluate the benefits of ...\nStudents should be able to read, write and transform data ...'}),
        }


class StrandCreateForm(forms.ModelForm):


    class Meta:
        model = Strand
        fields = ['title', 'colour', 'learning_outcome_list']
        widgets = WIDGETS
        labels = LABELS

    def clean_title(self):
        return profanity_clean_field(self, 'title')


class StrandUpdateForm(forms.ModelForm):


    class Meta:
        model = Strand
        fields = ['title', 'learning_outcome_list']
        widgets = WIDGETS
        labels = LABELS

    def clean_title(self):
        return profanity_clean_field(self, 'title')
