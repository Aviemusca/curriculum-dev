from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from django.urls import reverse_lazy

from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

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

from .models import Curriculum
from accounts.models import CustomUser

from .forms import CurriculumCreateForm, CurriculumUpdateForm

class CurriculumListView(ListView):
    """ List all the public curricula """
    model = Curriculum
    template_name = 'curriculum_list.html'
    paginate_by = 5
    # Return only public curricula prepended by admin curricula
    def get_queryset(self):
        super().get_queryset()
        admin_qs = Curriculum.objects.filter(author__is_staff=True).filter(public=True).order_by('-date_created')
        complement_public_qs = Curriculum.objects.exclude(author__is_staff=True).filter(public=True).order_by('-date_created')
        return list(admin_qs) + list(complement_public_qs)

class CurriculumDetailView(UserPassesTestMixin, DetailView):
    model = Curriculum
    template_name = 'curriculum_detail.html'
    slug_field = 'slug'
    slug_url_kwarg = 'slug_curriculum'

    def test_func(self):
        """ Ensure the user is the author or the curriculum is public """
        curriculum = self.get_object()
        return True if self.request.user == curriculum.author else curriculum.public

    def get_context_data(self, **kwargs):
        """ Return curriculum analysis data for chart rendering """
        context = super(CurriculumDetailView, self).get_context_data(**kwargs)
        curriculum = get_object_or_404(Curriculum, slug=self.kwargs.get('slug_curriculum'))
        context['analyses'] = curriculum.curriculum_analyses.all().order_by('-date_created')
        context['strands'] = curriculum.strands.all().order_by('date_created')
        return context

class CurriculumCreateView(LoginRequiredMixin, CreateView):
    model = Curriculum
    form_class = CurriculumCreateForm
    template_name = 'curriculum_form.html'

    def form_valid(self, form):
        """ Ensure the user requesting the view is saved in the form """
        form.instance.author = self.request.user
        return super(CurriculumCreateView, self).form_valid(form)


class CurriculumUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Curriculum
    form_class = CurriculumUpdateForm
    template_name = 'curriculum_update.html'
    slug_field = 'slug'
    slug_url_kwarg = 'slug_curriculum'

    def test_func(self):
        """ Ensure the user requesting the view is the author/creator """
        curriculum = self.get_object()
        return self.request.user == curriculum.author

    def form_valid(self, form):
        """ Ensure the user requesting the view is saved in the form """
        form.instance.author = self.request.user
        return super(CurriculumUpdateView, self).form_valid(form)


class CurriculumDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Curriculum
    template_name = 'curriculum_confirm_delete.html'
    slug_field = 'slug'
    slug_url_kwarg = 'slug_curriculum'

    def test_func(self):
        """ Ensure the user requesting the view is the author/creator """
        curriculum = self.get_object()
        return self.request.user == curriculum.author

    def form_valid(self, form):
        """ Ensure the user requisting the form is saved in the form """
        form.instance.author = self.request.user
        return super(CurriculumDeleteView, self).form_valid(form)

    def get_success_url(self):
        return reverse_lazy('curricula:user', kwargs={'username': self.get_object().author.username})

class UserCurriculumListView(LoginRequiredMixin, ListView):
    model = Curriculum
    template_name = 'curriculum_list.html'
    paginate_by = 5

    def get_queryset(self):
        """ Return only public curricula if the user is not the target author """
        target_author = get_object_or_404(CustomUser, username=self.kwargs.get('username', None))
        if self.request.user == target_author:
            return Curriculum.objects.filter(author=target_author)
        else:
            return Curriculum.objects.filter(author=target_author).filter(public=True)


@method_decorator(csrf_exempt, name='dispatch')
class CurriculumTogglePublic(LoginRequiredMixin, UserPassesTestMixin, View):
    """ A view to handle public/private toggling. Expects an AJAX call, which triggers the toggle """

    def test_func(self):
        """ Ensure the user rquesting the toggle is the author of the curriculum """
        curriculum = get_object_or_404(Curriculum, slug=self.kwargs.get('slug_curriculum', None))
        return self.request.user == curriculum.author

    def get(self, request, **kwargs):
        curriculum = get_object_or_404(Curriculum, slug=self.kwargs.get('slug_curriculum', None))
        # Toggle public/private state
        curriculum.public = not curriculum.public
        curriculum.save()
        data = {
                'result': 'Curriculum updated successfully!',
                'public': curriculum.public,
                }
        return JsonResponse(data)


