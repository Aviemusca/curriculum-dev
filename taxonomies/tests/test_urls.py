from django.urls import reverse, resolve

from django.test import SimpleTestCase

from taxonomies.views import (
        TaxonomyListView,
        TaxonomyDetailView,
        TaxonomyCreateView,
        TaxonomyUpdateView,
        TaxonomyDeleteView,
        UserTaxonomyListView,
        )


class TestUrls(SimpleTestCase):

    def test_taxonomy_home_page_resolves(self):
        url = reverse('taxonomies:home')
        self.assertEqual(resolve(url).func.view_class, TaxonomyListView)

    def test_user_taxonomy_list_page_resolves(self):
        url = reverse('taxonomies:user', kwargs={'username': 'user'})
        self.assertEqual(resolve(url).func.view_class, UserTaxonomyListView)

    def test_taxonomy_create_page_resolves(self):
        url = reverse('taxonomies:create')
        self.assertEqual(resolve(url).func.view_class, TaxonomyCreateView)

    def test_user_taxonomy_detail_page_resolves(self):
        url = reverse('taxonomies:detail', kwargs={'slug_taxonomy': 'slug'})
        self.assertEqual(resolve(url).func.view_class, TaxonomyDetailView)

    def test_user_taxonomy_update_page_resolves(self):
        url = reverse('taxonomies:update', kwargs={'slug_taxonomy': 'slug'})
        self.assertEqual(resolve(url).func.view_class, TaxonomyUpdateView)

    def test_user_taxonomy_delete_page_resolves(self):
        url = reverse('taxonomies:delete', kwargs={'slug_taxonomy': 'slug'})
        self.assertEqual(resolve(url).func.view_class, TaxonomyDeleteView)
