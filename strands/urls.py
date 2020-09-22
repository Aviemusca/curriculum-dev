from django.urls import path

from .views import (
        StrandCreateView,
        StrandListView,
        StrandDetailView,
        StrandUpdateView,
        StrandDeleteView,
        StrandUpdateColour,
        )

from . import views

urlpatterns = [
        # The pk_curriculum is passed in order to attach the strand to
        # the curriculum in StrandCreateView
        path('<int:pk_curriculum>/strand/new/', StrandCreateView.as_view(), name='create'),
        path('<int:pk_curriculum>/strands/', StrandListView.as_view(), name='list_curriculum'),
        path('<int:pk_curriculum>/strand/<slug:slug_strand>/', StrandDetailView.as_view(), name='detail'),
        path('<int:pk_curriculum>/strand/<slug:slug_strand>/update/', StrandUpdateView.as_view(), name='update'),
        path('<int:pk_curriculum>/strand/<slug:slug_strand>/delete/', StrandDeleteView.as_view(), name='delete'),
        path('<int:pk_curriculum>/strand/<slug:slug_strand>/update_colour/', StrandUpdateColour.as_view(), name='update_colour'),
        ]

