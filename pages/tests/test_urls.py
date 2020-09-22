from django.test import SimpleTestCase
from django.urls import reverse, resolve
from pages.views import HomePageView, AboutPageView

class TestUrls(SimpleTestCase):

    def test_home_url_resolves(self):
        url = reverse('pages:home')
        self.assertEquals(resolve(url).func.view_class, HomePageView)

    def test_about_url_resolves(self):
        url = reverse('pages:about')
        self.assertEquals(resolve(url).func.view_class, AboutPageView)


