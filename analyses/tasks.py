from __future__ import absolute_import, unicode_literals
from django.http import Http404

from .models import (
        CurriculumAnalysis,
        StrandAnalysis,
        LearningOutcomeAnalysis
        )

from LO_analysis_project.celery import app
from celery.utils import uuid
from celery import signature, chain, group, chord, current_task

@app.task
def analyse_curriculum(analysis_id, ignore_result=True):
    # Get the curriculum analysis or generate a 404 error
    try:
        curr_analysis = CurriculumAnalysis.objects.get(pk=analysis_id)
    except CurriculumAnalysis.DoesNotExist:
        raise Http404('The curriculum analysis does not exist!')
    else:
        # initialises non categorised verbs and strand analyses
        strand_analyses = curr_analysis.initialise()

        # Generate group (parallel) tasks carried over all the strands, using signatures
        lo_tasks = group(single_strand_lo_hit_count_analyses.si(strand_analysis.pk) for strand_analysis in strand_analyses)
        category_tasks = group(single_strand_category_hit_count_analysis.si(strand_analysis.pk) for strand_analysis in strand_analyses)
        diversity_tasks = group(single_strand_category_diversity_analysis.si(strand_analysis.pk) for strand_analysis in strand_analyses)
        average_tasks = group(single_strand_average_analysis.si(strand_analysis.pk) for strand_analysis in strand_analyses)

        # chain the group tasks i.e chord
        chain_tasks = chain(lo_tasks, category_tasks, diversity_tasks, average_tasks)

        result_chain = chain_tasks.apply_async()


@app.task(bind=True, name="analyses.tasks.task_complete")
def task_complete( self, results=None, *args, **kwargs ):
    return results

@app.task
def single_strand_category_diversity_analysis(analysis_id):
    try:
        strand_analysis = StrandAnalysis.objects.get(pk=analysis_id)
    except StrandAnaysis.DoesNotExist:
        raise Http404('The strand analysis does not exist!')
    else:
        strand_analysis.strand_category_diversity_analysis()

@app.task
def single_strand_category_hit_count_analysis(analysis_id):
    try:
        strand_analysis = StrandAnalysis.objects.get(pk=analysis_id)
    except StrandAnaysis.DoesNotExist:
        raise Http404('The strand analysis does not exist!')
    else:
        strand_analysis.strand_category_hit_count_analysis()

@app.task
def single_strand_average_analysis(analysis_id):
    try:
        strand_analysis = StrandAnalysis.objects.get(pk=analysis_id)
    except StrandAnaysis.DoesNotExist:
        raise Http404('The strand analysis does not exist!')
    else:
        strand_analysis.strand_average_analysis()

@app.task
def single_strand_lo_hit_count_analyses(analysis_id):
    try:
        strand_analysis = StrandAnalysis.objects.get(pk=analysis_id)
    except StrandAnaysis.DoesNotExist:
        raise Http404('The strand analysis does not exist!')
    else:
        lo_analyses = strand_analysis.initialise_learning_outcome_analyses()
        group(single_lo_hit_count_analysis.si(lo_analysis.pk) for lo_analysis in lo_analyses)()

@app.task
def single_lo_hit_count_analysis(analysis_id):
    try:
        lo_analysis = LearningOutcomeAnalysis.objects.get(pk=analysis_id)
    except LearningOutcomeAnalysis.DoesNotExist:
        raise Http404('The learning outcome analysis does not exist!')
    else:
        lo_analysis.hit_count_analysis()


