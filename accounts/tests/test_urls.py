from django.test import SimpleTestCase, TestCase
from django.urls import reverse, resolve
from accounts.views import SignUpView, profile

class TestUrls(SimpleTestCase):

    def test_sign_up_page_resolves(self):
        url = reverse('signup')
        self.assertEqual(resolve(url).func.view_class, SignUpView)

    def test_profile_page_resolves(self):
        url = reverse('profile')
        self.assertEqual(resolve(url).func, profile)
