from django.contrib import admin

from .models import LearningOutcome


class LearningOutcomeAdmin(admin.ModelAdmin):
    model = LearningOutcome
    readonly_fields = ('index', )


admin.site.register(LearningOutcome, LearningOutcomeAdmin)
