from django.urls import path, include

from .views import (
        TaxonomyListView,
        TaxonomyDetailView,
        TaxonomyCreateView,
        TaxonomyUpdateView,
        TaxonomyDeleteView,
        UserTaxonomyListView,
        VerbNumberDataView,
        TaxonomyOverlapDataView,
        TaxonomyTogglePublic,
        )
from . import views

urlpatterns = [
        path('', TaxonomyListView.as_view(), name='home'),
        path('<str:username>/', UserTaxonomyListView.as_view(), name='user'),
        path('taxonomy/new/', TaxonomyCreateView.as_view(), name='create'),
        path('taxonomy/<slug:slug_taxonomy>/', TaxonomyDetailView.as_view(), name='detail'),
        path('taxonomy/<slug:slug_taxonomy>/update/', TaxonomyUpdateView.as_view(), name='update'),
        path('taxonomy/<slug:slug_taxonomy>/delete/', TaxonomyDeleteView.as_view(), name='delete'),
        path('taxonomy/<slug:slug_taxonomy>/verb_number_data/', VerbNumberDataView.as_view(), name='verb_number_data'),
        path('taxonomy/<slug:slug_taxonomy>/overlap_data/', TaxonomyOverlapDataView.as_view(), name='overlap_data'),
        path('taxonomy/<slug:slug_taxonomy>/toggle_public/', TaxonomyTogglePublic.as_view(), name='toggle_public'),
        path('taxonomy/<slug:slug_taxonomy>/verb_categories/', include(('verb_categories.urls', 'verb_categories'), namespace='verb_categories')),
        ]
