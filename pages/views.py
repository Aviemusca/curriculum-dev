from django.urls import reverse_lazy
from django.views.generic import TemplateView, CreateView
from django.contrib.messages.views import SuccessMessageMixin

from .models import Contact
from curricula.models import Curriculum
from .forms import ContactForm

""" Views for the 'non-app' related pages of the site, e.g. home, about """

class HomePageView(TemplateView):
    template_name = 'home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Get the Admin Computer Science curriculum
        target_curriculum = Curriculum.objects.filter(author__username='admin').filter(title='Computer Science').first()
        context['object'] = target_curriculum
        context['analysis'] = target_curriculum.curriculum_analyses.all().first()
        return context


class AboutPageView(TemplateView):
    template_name = 'about.html'


class ContactPageView(SuccessMessageMixin, CreateView):
    model = Contact
    form_class = ContactForm
    template_name = 'contact.html'
    success_message = 'Thanks for getting in touch! We will try to get back to you soon.'
    success_url = reverse_lazy('pages:home')
