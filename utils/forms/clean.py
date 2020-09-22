from profanity_check import predict

from django import forms

def profanity_clean_field(form_instance, field):
    """ Checks for profanity in a specific form field """
    data = form_instance.cleaned_data.get(field)

    if predict([data])[0]:
        raise forms.ValidationError('Watch your mouth!')

    return data

def profanity_clean_fields(FormClass, form_instance):
    """ Checks for profanity in all fields of a form instance """
    cleaned_data = super(FormClass, form_instance).clean()
    for field in form_instance.fields.keys():
        if field and predict([cleaned_data.get(field)])[0]:
            raise forms.ValidationError('Watch your mouth!')
    return cleaned_data


