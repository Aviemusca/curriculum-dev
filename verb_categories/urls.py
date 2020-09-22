from django.urls import path

from .views import (
        VerbCategoryCreateView,
        VerbCategoryListView,
        VerbCategoryUpdateView,
        VerbCategoryDeleteView,
        )


urlpatterns = [
        # The pk_taxonomy is passed in order to attach the verb_category to
        # the taxonomy in VerbCategoryCreateView
        path('<int:pk_taxonomy>/verb_category/new/', VerbCategoryCreateView.as_view(), name='create'),
        path('<int:pk_taxonomy>/verb_categories/', VerbCategoryListView.as_view(), name='list_taxonomy'),
        path('<int:pk_taxonomy>/verb_category/<slug:slug_verb_category>/update/', VerbCategoryUpdateView.as_view(), name='update'),
        path('<int:pk_taxonomy>/verb_category/<slug:slug_verb_category>/delete/', VerbCategoryDeleteView.as_view(), name='delete'),
        ]

