from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.urls import reverse_lazy

from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

from django.views.generic import (
        View,
        DetailView,
        ListView,
        CreateView,
        UpdateView,
        DeleteView
        )

from .models import Strand
from curricula.models import Curriculum
from accounts.models import CustomUser

from .forms import StrandCreateForm, StrandUpdateForm

# Strand List and detail views are currently not accessible by user
# (no links and empty templates)

class StrandListView(ListView):
    """ A List View for all strands of a curriculum (not whole database) """

    model = Strand
    template_name = 'strand_list.html'

    def get_queryset(self):
        target_curriculum = get_object_or_404(Curriculum, pk=self.kwargs.get('pk_curriculum'))
        return Strand.objects.filter(curriculum=target_curriculum)


class StrandDetailView(DetailView):


    model = Strand
    template_name = 'strand_detail.html'
    slug_field = 'slug'
    slug_url_kwarg = 'slug_strand'

    def get_context_data(self, **kwargs):
        """ Return strand_analysis data for chart rendering """
        context = super(StrandDetailView, self).get_context_data(**kwargs)
        strand = get_object_or_404(Strand, slug=self.kwargs.get('slug_strand'))
        context['analyses'] = strand.strand_analyses.all()
        return context


class StrandCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):


    model = Strand
    form_class = StrandCreateForm
    template_name = 'strand_form.html'
    slug_field = 'slug'
    slug_url_kwarg = 'slug_curriculum'

    def test_func(self):
        """
        Ensure the user requesting the view is the author of the curriculum,
        we do this by passing the primary key of the curriculum into the view via kwargs
        """
        target_curriculum = get_object_or_404(Curriculum, pk=self.kwargs.get('pk_curriculum'))
        return self.request.user == target_curriculum.author

    def form_valid(self, form):
        """
        A strand is connected with a unique curriculum, so we ensure the appropriate
        curriculum gets saved automatically in the form by passing in its primary key
        into the view via kwargs

        """
        target_curriculum = get_object_or_404(Curriculum, pk=self.kwargs.get('pk_curriculum'))
        form.instance.curriculum = target_curriculum
        return super(StrandCreateView, self).form_valid(form)

    def get_success_url(self):
        target_curriculum = get_object_or_404(Curriculum, pk=self.kwargs.get('pk_curriculum'))
        return reverse_lazy('curricula:detail', kwargs={'slug_curriculum': target_curriculum.slug})

class StrandUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):


    model = Strand
    form_class = StrandUpdateForm
    template_name = 'strand_update.html'
    slug_field = 'slug'
    slug_url_kwarg = 'slug_strand'

    def test_func(self):
        """ Ensure the user requesting the view is the author of the strand/curriculum """
        strand = self.get_object()
        return self.request.user == strand.get_author()

    def form_valid(self, form):
        """ Ensure the original curriculum is saved in the form """
        form.instance.curriculum = self.get_object().curriculum
        return super(StrandUpdateView, self).form_valid(form)

    def get_success_url(self):
        target_curriculum = get_object_or_404(Curriculum, pk=self.kwargs.get('pk_curriculum'))
        return reverse_lazy('curricula:detail', kwargs={'slug_curriculum': target_curriculum.slug})


class StrandDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):


    model = Strand
    template_name = 'strand_confirm_delete.html'
    slug_field = 'slug'
    slug_url_kwarg = 'slug_strand'

    def test_func(self):
        """ Ensure the user requesting deletion is author of strand/curriculum """
        strand = self.get_object()
        return self.request.user == strand.get_author()

    def get_success_url(self):
        target_curriculum = get_object_or_404(Curriculum, pk=self.kwargs.get('pk_curriculum'))
        return reverse_lazy('curricula:detail', kwargs={'slug_curriculum': target_curriculum.slug})


@method_decorator(csrf_exempt, name='dispatch')
class StrandUpdateColour(LoginRequiredMixin, UserPassesTestMixin, View):
    """ A view to handle strand colour updates. Expects an AJAX call
    with the strand slug a colour """

    def test_func(self):
        """ Ensure the user requesting colour change is the author of the strand """
        strand = get_object_or_404(Strand, slug=self.kwargs.get('slug_strand', None))
        return self.request.user == strand.get_author()

    def get(self, request, **kwargs):
        data = {
                "nothing to see here": "Move along.."
                }
        return JsonResponse(data)

    def post(self, request, **kwargs):
        strand_slug = request.POST.get('strand_slug', None)
        colour = request.POST.get('colour', None)
        strand = get_object_or_404(Strand, slug=strand_slug)
        strand.colour = colour
        strand.save()
        data = {
                'result': 'Strand colour updated successfully!',
                'colour': strand.colour,
                }
        return JsonResponse(data)


