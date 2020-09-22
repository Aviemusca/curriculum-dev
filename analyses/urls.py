from django.urls import path

from .views import (
        CurriculumAnalysisCreateView,
        CurriculumAnalysisProgressView,
        CurriculumAnalysisUpdateView,
        CurriculumAnalysisDeleteView,
        CurriculumHitCountDataView,
        CurriculumDiversityDataView,
        CurriculumAverageVerbsDataView,
        CurriculumAverageCategoriesDataView,
        )
from . import views

urlpatterns = [
        path('<int:pk_curriculum>/analysis/new/', CurriculumAnalysisCreateView.as_view(), name='create'),
        path('<int:pk_curriculum>/<slug:slug_curriculum_analysis>/start_analysis', CurriculumAnalysisProgressView.as_view(), name='progress'),
        path('<int:pk_curriculum>/<slug:slug_curriculum_analysis>/update/', CurriculumAnalysisUpdateView.as_view(), name='update'),
        path('<int:pk_curriculum>/<slug:slug_curriculum_analysis>/delete/', CurriculumAnalysisDeleteView.as_view(), name='delete'),
        path('<int:pk_curriculum>/<slug:slug_curriculum_analysis>/curriculum_hit_count_data/', CurriculumHitCountDataView.as_view(), name='curriculum_hit_count_data'),
        path('<int:pk_curriculum>/<slug:slug_curriculum_analysis>/curriculum_diversity_data/', CurriculumDiversityDataView.as_view(), name='curriculum_diversity_data'),
        path('<int:pk_curriculum>/<slug:slug_curriculum_analysis>/curriculum_average_verbs_data/', CurriculumAverageVerbsDataView.as_view(), name='curriculum_average_verbs_data'),
        path('<int:pk_curriculum>/<slug:slug_curriculum_analysis>/curriculum_average_categories_data/', CurriculumAverageCategoriesDataView.as_view(), name='curriculum_average_categories_data'),
        path('<int:pk_curriculum>/<slug:slug_curriculum_analysis>/<str:task_id>/', views.curriculum_analysis_progress_data, name='curriculum_analysis_progress_data'),
        ]
