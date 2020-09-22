from django.urls import path, include

from .views import (
        CurriculumListView,
        CurriculumDetailView,
        CurriculumCreateView,
        CurriculumUpdateView,
        CurriculumDeleteView,
        UserCurriculumListView,
        CurriculumTogglePublic,
        )

urlpatterns = [
        path('', CurriculumListView.as_view(), name='home'),
        path('<str:username>/', UserCurriculumListView.as_view(), name='user'),
        path('curriculum/new/', CurriculumCreateView.as_view(), name='create'),
        path('curriculum/<slug:slug_curriculum>/', CurriculumDetailView.as_view(), name='detail'),
        path('curriculum/<slug:slug_curriculum>/update/', CurriculumUpdateView.as_view(), name='update'),
        path('curriculum/<slug:slug_curriculum>/delete/', CurriculumDeleteView.as_view(), name='delete'),
        path('curriculum/<slug:slug_curriculum>/strands/', include(('strands.urls', 'strands'), namespace='strands')),
        path('curriculum/<slug:slug_curriculum>/analyses/', include(('analyses.urls', 'analyses'), namespace='analyses')),
        path('curriculum/<slug:slug_curriculum>/toggle_public/', CurriculumTogglePublic.as_view(), name='toggle_public'),
        ]
