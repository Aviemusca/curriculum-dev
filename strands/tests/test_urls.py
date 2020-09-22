from django.urls import reverse, resolve
from django.test import SimpleTestCase

from strands.views import (
        StrandListView,
        StrandCreateView,
        StrandDetailView,
        StrandUpdateView,
        StrandDeleteView,
        )

class TestUrls(SimpleTestCase):

    def test_strand_curriculum_home_url_resolves(self):
        url = reverse('curricula:strands:list_curriculum', kwargs={'slug_curriculum': 'slug', 'pk_curriculum': '1'})
        self.assertEqual(resolve(url).func.view_class, StrandListView)

    def test_strand_create_url_resolves(self):
        url = reverse('curricula:strands:create', kwargs={'slug_curriculum': 'slug', 'pk_curriculum': '1'})
        self.assertEqual(resolve(url).func.view_class, StrandCreateView)

    def test_strand_detail_url_resolves(self):
        url = reverse('curricula:strands:detail', kwargs={'slug_curriculum': 'slug', 'slug_strand': 'slug', 'pk_curriculum': '1'})
        self.assertEqual(resolve(url).func.view_class, StrandDetailView)

    def test_strand_update_url_resolves(self):
        url = reverse('curricula:strands:update', kwargs={'slug_curriculum': 'slug', 'slug_strand': 'slug', 'pk_curriculum': '1'})
        self.assertEqual(resolve(url).func.view_class, StrandUpdateView)

    def test_strand_delete_url_resolves(self):
        url = reverse('curricula:strands:delete', kwargs={'slug_curriculum': 'slug', 'slug_strand': 'slug', 'pk_curriculum': '1'})
        self.assertEqual(resolve(url).func.view_class, StrandDeleteView)
