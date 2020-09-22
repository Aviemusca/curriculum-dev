from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy
from django.http import Http404, JsonResponse

from django.contrib import messages
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

from curricula.models import Curriculum
from .models import CurriculumAnalysis
from taxonomies.models import CustomUserTaxonomy as Taxonomy

import collections

from .tasks import analyse_curriculum, task_complete
from celery import chord
from celery.result import AsyncResult

from .forms import CurriculumAnalysisCreateForm, CurriculumAnalysisUpdateForm

# No Curriculum Analysis detail view as detail info is currently embedded
# in the curriculum detail view


class CurriculumAnalysisCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = CurriculumAnalysis
    form_class = CurriculumAnalysisCreateForm
    template_name = 'curriculum_analysis_form.html'

    def get_curriculum(self):
        """ Allows access to the curriculum in the template """
        target_curriculum = get_object_or_404(Curriculum, pk=self.kwargs.get('pk_curriculum'))
        return target_curriculum

    def test_func(self):
        """
        Need to ensure the user requesting the view is the author
        of the curriculum, so we pass in the curriculum primary key
        into the view via kwargs
        """
        target_curriculum = get_object_or_404(Curriculum, pk=self.kwargs.get('pk_curriculum'))
        return self.request.user == target_curriculum.author

    def get_form_kwargs(self, **kwargs):
        """ Pass the request to the form to filter taxonomies authored by the user """
        form_data = super().get_form_kwargs(**kwargs)
        form_data['request'] = self.request
        return form_data


    def form_valid(self, form):
        """
        A curriculum analysis is connected with a unique curriculum,
        so we ensure the appropriate curriculum gets saved automatically
        in the form by passing its primary key into the view via kwargs.
        """
        target_curriculum = get_object_or_404(Curriculum, pk=self.kwargs.get('pk_curriculum'))
        form.instance.curriculum = target_curriculum
        return super(CurriculumAnalysisCreateView, self).form_valid(form)

    def get_success_url(self):
        target_curriculum = get_object_or_404(Curriculum, pk=self.kwargs.get('pk_curriculum'))
        return reverse_lazy('curricula:analyses:progress', kwargs={'slug_curriculum': target_curriculum.slug, 'pk_curriculum': target_curriculum.pk, 'slug_curriculum_analysis': self.object.slug})


class CurriculumAnalysisProgressView(LoginRequiredMixin, UserPassesTestMixin, TemplateView):
    """ A view which triggers a cuccirulum_analysis celery task and returns the task id to the template """

    def get(self, request, **kwargs):

        target_analysis = get_object_or_404(CurriculumAnalysis, slug=self.kwargs.get('slug_curriculum_analysis'))
        try:
            curriculum = target_analysis.get_curriculum()
        except Curriculum.DoesNotExist:
            raise Http404("The curriculum does not exist!")
        else:
            task = analyse_curriculum.si(target_analysis.pk)
            callback = task_complete.si()
            callback_task_id = chord(task)(callback)
            context = {
                'task_id': callback_task_id,
                'analysis': target_analysis,
                }
            return render(request, template_name="curriculum_analysis_progress.html", context=context)

    def test_func(self):
        """
        Need to ensure the user requesting the view is the author
        of the curriculum, so we pass in the curriculum primary key
        into the view via kwargs
        """
        target_curriculum = get_object_or_404(Curriculum, pk=self.kwargs.get('pk_curriculum'))
        return self.request.user == target_curriculum.author


class CurriculumAnalysisUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = CurriculumAnalysis
    form_class = CurriculumAnalysisUpdateForm
    template_name = 'curriculum_analysis_update.html'
    slug_field = 'slug'
    slug_url_kwarg = 'slug_curriculum_analysis'

    def test_func(self):
        """ Ensure the user requesting the view is the author of the curriculum """
        curriculum = self.get_object().curriculum
        return self.request.user == curriculum.author

    def get_form_kwargs(self, **kwargs):
        """ Pass the request to the form to filter taxonomies authored by the user """
        form_data = super().get_form_kwargs(**kwargs)
        form_data['request'] = self.request
        return form_data

    def form_valid(self, form):
        """ Ensure the curriculum is saved in the form """
        form.instance.curriculum = self.get_object().curriculum
        return super(CurriculumAnalysisUpdateView, self).form_valid(form)

    def get_success_url(self):
        target_curriculum = get_object_or_404(Curriculum, pk=self.kwargs.get('pk_curriculum'))
        return reverse_lazy('curricula:analyses:progress', kwargs={'slug_curriculum': target_curriculum.slug, 'pk_curriculum': target_curriculum.pk, 'slug_curriculum_analysis': self.object.slug})


class CurriculumAnalysisDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = CurriculumAnalysis
    template_name = 'curriculum_analysis_confirm_delete.html'
    slug_field = 'slug'
    slug_url_kwarg = 'slug_curriculum_analysis'

    def test_func(self):
        """ Ensure the user requesting the view is the author of the curriculum """
        curriculum = self.get_object().curriculum
        return self.request.user == curriculum.author

    def get_success_url(self):
        target_curriculum = get_object_or_404(Curriculum, pk=self.kwargs.get('pk_curriculum'))
        return reverse_lazy('curricula:detail', kwargs={'slug_curriculum': target_curriculum.slug})


class CurriculumDataMixin:
    """ A mixin for curriculum analysis data  aggregation views """

    def test_permissions(self):
        """ Ensure the curriculum is public """
        curriculum_analysis = self.get_curriculum_analysis()
        return True if self.request.user == curriculum_analysis.get_author() else curriculum_analysis.get_curriculum().public

    def get_curriculum_analysis(self, **kwargs):
        """ Get the target curriculum analysis """
        slug_analysis = self.kwargs.get('slug_curriculum_analysis', None)
        if slug_analysis is not None:
            analysis = get_object_or_404(CurriculumAnalysis, slug=slug_analysis)
        return analysis

    def get_ordered_verb_categories(self, taxonomy, **kwargs):
        """ Get the verb categories of a taxonomy ordered by level of abstraction """
        return [verb_cat.title for verb_cat in taxonomy.verb_categories.all().order_by('level')]

    def get_ordered_strands(self, curriculum_analysis, **kwargs):
        """ Get the strands ordered by strand date creation """
        return curriculum_analysis.curriculum.strands.all().order_by('date_created')

    def get_ordered_strand_analyses(self, curriculum_analysis, ordered_strands, **kwargs):
        """ Get the strand analyses of a curricuum analysis ordered by strand date creation """
        return [strand_analysis for strand in ordered_strands for strand_analysis in curriculum_analysis.strand_analyses.all() if strand_analysis.strand == strand]

    def get_ordered_strand_colours(self, ordered_strands, **kwargs):
        """ Get the ordered strand colours """
        return [strand.colour for strand in ordered_strands]

class CurriculumHitCountDataView(CurriculumDataMixin, UserPassesTestMixin, View):

    """ Aggregate data and return a JSON response for curriculum analysis chart rendering """

    def test_func(self):
        return self.test_permissions()

    def get(self, request, **kwargs):
        # Get the target curriculum analysis and taxonomy
        curriculum_analysis = self.get_curriculum_analysis()
        taxonomy = curriculum_analysis.get_taxonomy()

        # Order the verb categories by level of abstraction
        verb_cats = self.get_ordered_verb_categories(taxonomy)

        strands = self.get_ordered_strands(curriculum_analysis)

        # Order the strand analyses by strand date creation (inverse to curriculum grid side-bar)
        strand_analyses = self.get_ordered_strand_analyses(curriculum_analysis, strands)

        # Get the total num of los and strand colours (ordered as above)
        num_los = curriculum_analysis.get_num_learning_outcomes()
        colours = self.get_ordered_strand_colours(strands)

        # Order the category occurrences for each strand in the same order as above
        category_hit_counts = [strand_analysis.get_category_hit_counts() for strand_analysis in strand_analyses]

        # Get the category hits for each strand and verb category, ordered by strand (creation date) and cat level
        data = []
        for index, strand in enumerate(category_hit_counts):
            data.append([])
            data[index] = [strand.get(cat) for cat in verb_cats]

        return JsonResponse(data={
            'labels': verb_cats,
            'colours': colours,
            'data': data,
            'numLOs': num_los,
            'analysisPk': curriculum_analysis.pk,
            })

class CurriculumDiversityDataView(CurriculumDataMixin, UserPassesTestMixin, View):
    """ Aggregate data and return a JSON response for curriculum diversity chart rendering """

    def test_func(self):
        return self.test_permissions()

    def get(self, request, **kwargs):
        # Get the target curriculum analysis and total number of verb categories
        curriculum_analysis = self.get_curriculum_analysis()
        num_categories = curriculum_analysis.get_taxonomy().verb_categories.count()

        # Order the strand analyses by strand date creation (inverse to curriculum grid side-bar)
        strands = self.get_ordered_strands(curriculum_analysis)
        strand_analyses = self.get_ordered_strand_analyses(curriculum_analysis, strands)

        # Get the total number of los and strand colours (ordered as above)
        num_los = curriculum_analysis.get_num_learning_outcomes()
        colours = self.get_ordered_strand_colours(strands)

        # Order the category diversities for each strand in the same order as above
        category_diversities = [strand_analysis.get_category_diversities() for strand_analysis in strand_analyses]

        # Labels are numbers of verb categories
        labels = [i for i in range(0, num_categories + 1)]

        # Get the category diversities for each strand and category number, ordered by strand (creation date) and cat number
        data = []
        for index, strand in enumerate(category_diversities):
            data.append([])
            data[index] = [strand.get(label) for label in labels]

        return JsonResponse(data={
            'labels': labels,
            'colours': colours,
            'data': data,
            'numLOs': num_los,
            'analysisPk': curriculum_analysis.pk,
            })


class CurriculumAverageVerbsDataView(CurriculumDataMixin, UserPassesTestMixin, View):
    """ Return a JSON response giving the average verbs per lo (over each strand) of a curriculum analysis """

    def test_func(self):
        return self.test_permissions()

    def get(self, request, **kwargs):
        # Get the target curriculum analysis
        curriculum_analysis = self.get_curriculum_analysis()

        # Order the strand analyses by strand date creation (inverse to curriculum grid side-bar)
        strands = self.get_ordered_strands(curriculum_analysis)
        strand_analyses = self.get_ordered_strand_analyses(curriculum_analysis, strands)

        # Get the strand colours (ordered as above)
        colours = self.get_ordered_strand_colours(strands)

        # Order the verb averages averages for each strand in the same order as above
        verb_averages = [strand_analysis.get_verb_average() for strand_analysis in strand_analyses] # A list of average verb number in each strand

        # Labels are blank but needed for chartjs (length equal to num of strands)
        labels = ["" for _ in range(len(strand_analyses))]

        # Get the averages for each strand, ordered by strand creation date
        data = [strand_average.get(average) for strand_average in verb_averages for average in strand_average]

        return JsonResponse(data={
            'colours': colours,
            'labels': labels,
            'data': data,
            'analysisPk': curriculum_analysis.pk,
            })

class CurriculumAverageCategoriesDataView(CurriculumDataMixin, UserPassesTestMixin, View):
    """ Return a JSON response giving the average categories per lo (over each strand) of a curriculum analysis """
    def test_func(self):
        return self.test_permissions()

    def get(self, request, **kwargs):
        # Get the target curriculum analysis
        curriculum_analysis = self.get_curriculum_analysis()

        # Order the strand analyses by strand date creation (inverse to curriculum grid side-bar)
        strands = self.get_ordered_strands(curriculum_analysis)
        strand_analyses = self.get_ordered_strand_analyses(curriculum_analysis, strands)

        # Get the strand colours (ordered as above)
        colours = self.get_ordered_strand_colours(strands)

        # Order the category averages for each strand in the same order as above
        category_averages = [strand_analysis.get_category_average() for strand_analysis in strand_analyses] # A list of average category number in each strand


        # Labels are blank but needed for chartjs (length equal to num of strands)
        labels = ["" for _ in range(len(strand_analyses))]

        # Get the averages for each strand, ordered by strand creation date
        data = [strand_average.get(average) for strand_average in category_averages for average in strand_average]

        return JsonResponse(data={
            'colours': colours,
            'labels': labels,
            'data': data,
            'analysisPk': curriculum_analysis.pk,
            })

def curriculum_analysis_progress_data(request, **kwargs):
    """ Return a JSON response giving the status of a curriculum analysis task """
    analysis_task = AsyncResult(kwargs.get('task_id'))
    task_status = analysis_task.status
    return JsonResponse(data={
        'taskStatus': task_status,
        })


