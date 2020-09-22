from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.http import JsonResponse

from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin

from django.views.generic import (
        View,
        TemplateView,
        ListView,
        DetailView,
        CreateView,
        UpdateView,
        DeleteView
        )

from .models import CustomUserTaxonomy as Taxonomy
from accounts.models import CustomUser

from .forms import TaxonomyCreateForm, TaxonomyUpdateForm

class TaxonomyListView(ListView):
    """ List all the public taxonomies """
    model = Taxonomy
    template_name = 'taxonomy_list.html'
    paginate_by = 5
    # Return only public taxonomies prepended by admin taxonomies
    def get_queryset(self):
        super().get_queryset()
        admin_qs = Taxonomy.objects.filter(author__username='admin').filter(public=True).order_by('-date_created')
        complement_public_qs = Taxonomy.objects.exclude(author__username='admin').filter(public=True).order_by('-date_created')
        return list(admin_qs) + list(complement_public_qs)



class TaxonomyDetailView(DetailView):
    model = Taxonomy
    template_name = 'taxonomy_detail.html'
    slug_field = 'slug'
    slug_url_kwarg = 'slug_taxonomy'


class TaxonomyCreateView(LoginRequiredMixin, CreateView):
    model = Taxonomy
    form_class = TaxonomyCreateForm
    template_name = 'taxonomy_form.html'

    def form_valid(self, form):
        """ Ensure the user requesting the view is saved in the form """
        form.instance.author = self.request.user
        return super(TaxonomyCreateView, self).form_valid(form)


class TaxonomyUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Taxonomy
    form_class = TaxonomyUpdateForm
    template_name = 'taxonomy_update.html'
    slug_field = 'slug'
    slug_url_kwarg = 'slug_taxonomy'

    def test_func(self):
        """ Ensure the user requesting the view is the author/creator """
        taxonomy = self.get_object()
        return self.request.user == taxonomy.author

    def form_valid(self, form):
        """ Ensure the user requesting the view is saved in the form """
        form.instance.author = self.request.user
        return super(TaxonomyUpdateView, self).form_valid(form)


class TaxonomyDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Taxonomy
    template_name = 'taxonomy_confirm_delete.html'
    slug_field = 'slug'
    slug_url_kwarg = 'slug_taxonomy'

    def test_func(self):
        """ Ensure the user requesting the view is the author/creator """
        taxonomy = self.get_object()
        return self.request.user == taxonomy.author

    def get_success_url(self):
        return reverse_lazy('taxonomies:user', kwargs={'username': self.get_object().author.username})

class UserTaxonomyListView(LoginRequiredMixin, ListView):
    model = Taxonomy
    template_name = 'taxonomy_list.html'
    paginate_by = 5

    def get_queryset(self):
        """ Return only public taxonomies if the user is not the target author """
        target_author = get_object_or_404(CustomUser, username=self.kwargs.get('username', None))
        if self.request.user == target_author:
            return Taxonomy.objects.filter(author=target_author)
        else:
            return Taxonomy.objects.filter(author=target_author).filter(public=True)


class TaxonomyDataMixin:
    """ A mixin for taxonomy data aggrgation views """

    def test_permissions(self):
        """ Ensure the taxonomy is public """
        taxonomy = self.get_taxonomy()
        return True if self.request.user == taxonomy.author else taxonomy.public

    def get_taxonomy(self, **kwargs):
        """ Get the target taxonomy from the url """
        slug_taxonomy = self.kwargs.get('slug_taxonomy', None)
        if slug_taxonomy is not None:
            taxonomy = get_object_or_404(Taxonomy, slug=slug_taxonomy)
        return taxonomy

    def get_ordered_verb_categories(self, taxonomy, **kwargs):
        """ Get the verb categories of a taxonomy ordered by level of abstraction """
        return [verb_cat for verb_cat in taxonomy.verb_categories.all().order_by('level')]


class VerbNumberDataView(TaxonomyDataMixin, UserPassesTestMixin, View):
    """ Returns a JSON response giving the number of elements(verbs and non-verbs)
    in each category """

    def test_func(self):
        return self.test_permissions()

    def get(self, request, **kwargs):
        # Get the target taxonomy
        taxonomy = self.get_taxonomy()

        # Order the verb categories by level of abstraction
        verb_cats = self.get_ordered_verb_categories(taxonomy)

        # Get the number of elements in each category
        num_elements = [verb_cat.get_num_elements() for verb_cat in verb_cats]

        # Define the labels
        labels = [verb_cat.title for verb_cat in verb_cats]

        return JsonResponse(data={
            'labels': labels,
            'data': num_elements,
            'analysisPk': taxonomy.pk,
            })

class TaxonomyOverlapDataView(TaxonomyDataMixin, UserPassesTestMixin, View):
    """ Returns a JSON response for chord charts relating to the overlap of the taxonomy  """
    def test_func(self):
        return self.test_permissions()

    def get(self, request, **kwargs):
        # Get the target taxonomy
        taxonomy = self.get_taxonomy()

        # Order the verb categories by level of abstraction
        verb_cats = self.get_ordered_verb_categories(taxonomy)

        # Define the labels
        labels = [verb_cat.title for verb_cat in verb_cats]

        # Generate the chord flow matrix data
        data = []
        for cat_i in verb_cats:
            data.append([cat_i.diagonal_verbs() if cat_i == cat_j else cat_i.overlap(cat_j) for cat_j in verb_cats])

        return JsonResponse(data={
            'labels': labels,
            'data': data,
            'analysisPk': taxonomy.pk,
            })


@method_decorator(csrf_exempt, name='dispatch')
class TaxonomyTogglePublic(TaxonomyDataMixin, LoginRequiredMixin, UserPassesTestMixin, View):
    """ A view to handle public/private toggling. Expects an AJAX call, which triggers the toggle """

    def test_func(self):
        """ Ensure the user rquesting the toggle is the author of the curriculum """
        taxonomy = self.get_taxonomy()
        return self.request.user == taxonomy.author

    def get(self, request, **kwargs):
        taxonomy = self.get_taxonomy()
        # Toggle public/private state
        taxonomy.public = not taxonomy.public
        taxonomy.save()
        data = {
                'result': 'Taxonomy updated successfully!',
                'public': taxonomy.public,
                }
        return JsonResponse(data)

