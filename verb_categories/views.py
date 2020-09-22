from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy

from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin

from django.views.generic import (
        DetailView,
        ListView,
        CreateView,
        UpdateView,
        DeleteView
        )


from .models import VerbCategory
from taxonomies.models import CustomUserTaxonomy as Taxonomy
from accounts.models import CustomUser

from .forms import VerbCategoryCreateForm, VerbCategoryUpdateForm


class VerbCategoryViewMixin:
    """ A mixin for the verb category views """

    def get_target_taxonomy(self):
        """ Returns the taxonomy connected with the verb category,
        whose pk is passed to the view by url """
        return get_object_or_404(Taxonomy, pk=self.kwargs.get('pk_taxonomy', None))

    def test_func_(self):
        """
        Need to ensure the user requesting the view is the author of the taxonomy,
        so we pass in the taxonomy primary key via kwargs
        """
        return self.request.user == self.get_target_taxonomy().author

    def get_form_kwargs_(self, ViewClass, **kwargs):
        """
        Each verb category should have a unique 'level' field, so we pass in
        the taxonomy to the form to perform validations.
        """
        form_data = super(ViewClass, self).get_form_kwargs(**kwargs)
        form_data['taxonomy'] = self.get_target_taxonomy()
        # If updating, pass the verb category to the form to allow user
        # to re-enter the same level value
        if ViewClass == VerbCategoryUpdateView:
            form_data['category'] = self.get_object()
        return form_data

    def form_valid_(self, ViewClass, form):
        """
        A verb category is connected with a unique taxonomy, so we
        ensure the appropriate taxonomy gets saved automatically in
        the form by passing in its primary key into the view via url kwargs

        """
        form.instance.taxonomy = self.get_target_taxonomy()
        return super(ViewClass, self).form_valid(form)

    def get_success_url_(self):
        target_taxonomy = self.get_target_taxonomy()
        return reverse_lazy('taxonomies:detail', kwargs={'slug_taxonomy': target_taxonomy.slug})


class VerbCategoryListView(VerbCategoryViewMixin, ListView):
    """ A List View for all Verb Categories of a taxonomy
    (and not all verb categories in the database) """

    model = VerbCategory
    template_name = 'verb_category_list.html'

    def get_queryset(self):
        return VerbCategory.objects.filter(taxonomy=self.get_target_taxonomy())


class VerbCategoryCreateView(
        VerbCategoryViewMixin,
        LoginRequiredMixin,
        UserPassesTestMixin,
        CreateView
        ):

    model = VerbCategory
    form_class = VerbCategoryCreateForm
    template_name = 'verb_category_form.html'

    def test_func(self):
        return self.test_func_()

    def get_form_kwargs(self, **kwargs):
        return self.get_form_kwargs_(VerbCategoryCreateView, **kwargs)

    def form_valid(self, form):
        return self.form_valid_(VerbCategoryCreateView, form)

    def get_success_url(self):
        return self.get_success_url_()


class VerbCategoryUpdateView(
        VerbCategoryViewMixin,
        LoginRequiredMixin,
        UserPassesTestMixin,
        UpdateView
        ):

    model = VerbCategory
    form_class = VerbCategoryUpdateForm
    template_name = 'verb_category_update.html'
    slug_field = 'slug'
    slug_url_kwarg = 'slug_verb_category'

    def test_func(self):
        return self.test_func_()

    def get_form_kwargs(self, **kwargs):
        return self.get_form_kwargs_(VerbCategoryUpdateView, **kwargs)

    def form_valid(self, form):
        return self.form_valid_(VerbCategoryUpdateView, form)

    def get_success_url(self):
        return self.get_success_url_()


class VerbCategoryDeleteView(
        VerbCategoryViewMixin,
        LoginRequiredMixin,
        UserPassesTestMixin,
        DeleteView
        ):

    model = VerbCategory
    template_name = 'verb_category_confirm_delete.html'
    slug_field = 'slug'
    slug_url_kwarg = 'slug_verb_category'

    def test_func(self):
        return self.test_func_()

    def get_success_url(self):
        return self.get_success_url_()

