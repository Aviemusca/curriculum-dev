from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm

from .models import CustomUser, Profile

from utils.forms.clean import profanity_clean_field

LABELS = {
        'username': 'Username*',
        'email': 'Email address*',
        'password1': 'Password*',
        }
class CustomUserFormMixin:
    """ A mixin for the custom user forms """

    def clean_username_(self):
        """ Cast all username to lowercase. Check for profanity also """
        submitted_username = self.cleaned_data.get('username', None)
        if submitted_username:
            self.cleaned_data['username'] = submitted_username.lower()
        return profanity_clean_field(self, 'username')

class CustomUserCreationForm(CustomUserFormMixin, UserCreationForm):


    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = ['username', 'email']
        labels = LABELS

    def clean_username(self):
        return self.clean_username_()

class CustomUserChangeForm(CustomUserFormMixin, UserChangeForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        password = self.fields.get('password')
        if password:
            password.help_text = password.help_text.replace(
                    '/password/', '/password_change/'
                    )

    class Meta:
        model = CustomUser
        fields = ['username', 'email']
        labels = LABELS

    def clean_username(self):
        return self.clean_username_()

class ProfileChangeForm(forms.ModelForm):


    class Meta:
        model = Profile
        fields = ['image']



