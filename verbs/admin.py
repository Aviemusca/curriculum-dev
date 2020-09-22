from django.contrib import admin

from .models import Verb, NonVerb, NonCatVerb

admin.site.register(Verb)
admin.site.register(NonVerb)
admin.site.register(NonCatVerb)
