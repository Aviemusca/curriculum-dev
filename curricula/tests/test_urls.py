from django.urls import reverse, resolve
from django.test import SimpleTestCase

from curricula.views import (
        CurriculumListView,
        UserCurriculumListView,
        CurriculumCreateView,
        CurriculumDetailView,
        CurriculumUpdateView,
        CurriculumDeleteView,
        )

class TestUrls(SimpleTestCase):

    def test_curriculum_home_url_resolves(self):
        url = reverse('curricula:home')
        self.assertEqual(resolve(url).func.view_class, CurriculumListView)

    def test_curriculum_user_list_url_resolves(self):
        url = reverse('curricula:user', kwargs={'username': 'user'})
        self.assertEqual(resolve(url).func.view_class, UserCurriculumListView)

    def test_curriculum_create_url_resolves(self):
        url = reverse('curricula:create')
        self.assertEqual(resolve(url).func.view_class, CurriculumCreateView)

    def test_curriculum_detail_url_resolves(self):
        url = reverse('curricula:detail', kwargs={'slug_curriculum': 'slug'})
        self.assertEqual(resolve(url).func.view_class, CurriculumDetailView)

    def test_curriculum_update_url_resolves(self):
        url = reverse('curricula:update', kwargs={'slug_curriculum': 'slug'})
        self.assertEqual(resolve(url).func.view_class, CurriculumUpdateView)

    def test_curriculum_delete_url_resolves(self):
        url = reverse('curricula:delete', kwargs={'slug_curriculum': 'slug'})
        self.assertEqual(resolve(url).func.view_class, CurriculumDeleteView)
