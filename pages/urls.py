from django.urls import path
from .views import HomePageView, AboutPageView, ContactPageView, home_page_data
from django.views.generic import TemplateView

urlpatterns = [
        path('', HomePageView.as_view(), name='home'),
        path('home-data', home_page_data, name='home_data'),
        path('about/', AboutPageView.as_view(), name='about'),
        path('contact/', ContactPageView.as_view(), name='contact'),
        path('blank/', TemplateView.as_view(template_name='blank.html'))
        ]
