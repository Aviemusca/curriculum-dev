from django.contrib import admin

from .models import Curriculum

class CurriculumAdmin(admin.ModelAdmin):
    model = Curriculum
    readonly_fields=('id',)

admin.site.register(Curriculum, CurriculumAdmin)
