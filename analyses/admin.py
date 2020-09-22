from django.contrib import admin

from .models import (
        CurriculumAnalysis,
        StrandAnalysis,
        LearningOutcomeAnalysis,
        LearningOutcomeCategoryHitCount,
        StrandCategoryHitCount,
        )

admin.site.register(CurriculumAnalysis)
admin.site.register(StrandAnalysis)
admin.site.register(LearningOutcomeAnalysis)
admin.site.register(LearningOutcomeCategoryHitCount)
admin.site.register(StrandCategoryHitCount)
