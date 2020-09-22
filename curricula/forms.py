from django import forms

from django_countries.widgets import CountrySelectWidget

from .models import Curriculum


ISCED_LEVEL_CHOICES = [
        ("Pre-primary education", "Pre-primary education"),
        ("Primary education", "Primary education"),
        ("Lower secondary education", "Lower secondary education"),
        ("Upper secondary education", "Upper secondary education"),
        ("Post-secondary non-tertiary education", "Post-secondary non-tertiary education"),
        ("First stage of tertiary education", "First stage of tertiary education"),
        ("Second stage of tertiary education", "Second stage of tertiary education"),
        ]

ISCED_WIKI_URL = "https://en.wikipedia.org/wiki/International_Standard_Classification_of_Education"

LABELS = {
        "title": "Title* \
                <span class='text-muted'><small>(Enter the title of the curriculum)</small></span>",
        "country": "Country* \
                <span class='text-muted'><small>(Enter the country of origin of the curriculum)</small></span>",
        "isced_level": f"ISCED level* \
                <span class='text-muted'><small>(Enter the <a href={ISCED_WIKI_URL} target='_blank'><abbr title='International Standard Classification of Education'>ISCED</abbr></a> level of the curriculum)</small></span>",
        "public": "Public \
                <span class='text-muted'><small>(Public curricula may be viewed by others)</small></span>",
                }


class CurriculumCreateForm(forms.ModelForm):


    class Meta:
        model = Curriculum
        fields = ['title', 'country', 'isced_level', 'public']
        widgets = {
                'title': forms.TextInput(attrs={'placeholder': 'e.g. Computer Science'}),
                'country': CountrySelectWidget(),
                'isced_level': forms.Select(choices=ISCED_LEVEL_CHOICES),
                }
        labels = LABELS

class CurriculumUpdateForm(forms.ModelForm):


    class Meta:
        model = Curriculum
        fields = ['title', 'country', 'isced_level', 'public']
        widgets = {
                'isced_level': forms.Select(choices=ISCED_LEVEL_CHOICES),
                }
        labels = LABELS
