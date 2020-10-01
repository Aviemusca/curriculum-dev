from django.urls import reverse_lazy
from django.views.generic import TemplateView, CreateView
from django.contrib.messages.views import SuccessMessageMixin
from django.http import JsonResponse

from .models import Contact
from curricula.models import Curriculum
from .forms import ContactForm

""" Views for the 'non-app' related pages of the site, e.g. home, about """

class HomePageView(TemplateView):
    template_name = 'home.html'


class AboutPageView(TemplateView):
    template_name = 'about.html'


class ContactPageView(SuccessMessageMixin, CreateView):
    model = Contact
    form_class = ContactForm
    template_name = 'contact.html'
    success_message = 'Thanks for getting in touch! We will try to get back to you soon.'
    success_url = reverse_lazy('pages:home')


def home_page_data(request, **kwargs):
    """ Return a JSON response with dummy curriculum analysis data for home page chart """
    labels = ["Knowledge", "Comprehension", "Application", "Analysis", "Synthesis", "Evaluation"]
    colours = ["AC2CAC", "4C4CD5", "257795"]
    data = [[11, 9, 13, 7, 3, 6], [11, 9, 18, 8, 4, 3], [2, 6, 11, 2, 8, 3]]
    return JsonResponse(data={
        "labels": labels,
        "colours": colours,
        "data": data,
        "numLOs": 59,
        "analysisPk": '#home',
        })
