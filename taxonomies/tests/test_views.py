from django.test import TestCase

from django.urls import reverse

from django.contrib.auth import get_user_model
from taxonomies.models import CustomUserTaxonomy as Taxonomy
from strands.models import Strand


class TaxonomyListViewTests(TestCase):
    """ List the taxonomies """
    def setUp(self):
        """ Create a user (for taxonomy) and taxonomy """
        self.credentials = {
                'username': 'newuser',
                'email': 'newuser@email.com',
                'password': 'secret',
                }
        self.new_user = get_user_model().objects.create_user(**self.credentials)
        self.new_taxonomy = Taxonomy.objects.create(
                title='test taxonomy',
                author=self.new_user,
                )
        self.url = reverse('taxonomies:home')

    def test_page_status_code(self):
        response = self.client.get(f'/taxonomies/')
        self.assertEqual(response.status_code, 200)

    def test_page_status_code_by_url_name(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_view_template(self):
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, 'taxonomy_list.html')

class TaxonomyDetailViewTests(TestCase):
    def setUp(self):
        """ Create a user (for taxonomy) and taxonomy """
        self.credentials = {
                'username': 'newuser',
                'email': 'newuser@email.com',
                'password': 'secret',
                }
        self.new_user = get_user_model().objects.create_user(**self.credentials)
        self.new_taxonomy = Taxonomy.objects.create(
                title='test taxonomy',
                author=self.new_user,
                )
        self.url = reverse('taxonomies:detail', kwargs={'slug_taxonomy': self.new_taxonomy.slug})

    def test_page_status_code(self):
        response = self.client.get(f'/taxonomies/taxonomy/{self.new_taxonomy.slug}/')
        self.assertEqual(response.status_code, 200)

    def test_page_status_code_by_url_name(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_view_template(self):
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, 'taxonomy_detail.html')


class TaxonomyCreateViewTestsNotAuthenticated(TestCase):

    def test_page_status_code(self):
        response = self.client.get(f'/taxonomies/taxonomy/new/')
        self.assertEqual(response.status_code, 302)

    def test_page_status_code_by_url_name(self):
        response = self.client.get(reverse('taxonomies:create'))
        self.assertEqual(response.status_code, 302)

    def test_redirect(self):
        response = self.client.get(reverse('taxonomies:create'))
        self.assertRedirects(response, f"{reverse('login')}?next={reverse('taxonomies:create')}", target_status_code=200)


class TaxonomyCreateViewTestsAuthenticated(TestCase):

    def setUp(self):
        """ Create a user """
        self.credentials = {
                'username': 'newuser',
                'email': 'newuser@email.com',
                'password': 'secret',
                }
        self.new_user = get_user_model().objects.create_user(**self.credentials)
        #Login the user
        self.client.post(reverse('login'), self.credentials, follow=True)

    def test_page_status_code(self):
        response = self.client.get(f'/taxonomies/taxonomy/new/')
        self.assertEqual(response.status_code, 200)

    def test_page_status_code_by_url_name(self):
        response = self.client.get(reverse('taxonomies:create'))
        self.assertEqual(response.status_code, 200)

    def test_view_template(self):
        response = self.client.get(reverse('taxonomies:create'))
        self.assertTemplateUsed(response, 'taxonomy_form.html')


class TaxonomyUpdateViewTestsNotAuthenticated(TestCase):

    def setUp(self):
        """ Create a user (for taxonomy) and taxonomy """
        self.credentials = {
                'username': 'newuser',
                'email': 'newuser@email.com',
                'password': 'secret',
                }
        self.new_user = get_user_model().objects.create_user(**self.credentials)
        self.new_taxonomy = Taxonomy.objects.create(
                title='test taxonomy',
                author=self.new_user,
                )
        self.url = reverse('taxonomies:update', kwargs={'slug_taxonomy': self.new_taxonomy.slug})

    def test_page_status_code(self):
        response = self.client.get(f'/taxonomies/taxonomy/{self.new_taxonomy.slug}/update/')
        self.assertEqual(response.status_code, 302)

    def test_page_status_code_by_url_name(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 302)

    def test_redirect(self):
        response = self.client.get(self.url)
        self.assertRedirects(response, f"{reverse('login')}?next={self.url}", target_status_code=200)


class TaxonomyUpdateViewTestsForbiddenUser(TestCase):

    def setUp(self):
        """ Create 2 users and a taxonomy """
        self.forbidden_user_credentials = {
                'username': 'forbidden_user',
                'email': 'forbidden_user@email.com',
                'password': 'secret',
                }
        self.author_credentials = {
                'username': 'author',
                'email': 'author@email.com',
                'password': 'secret',
                }
        self.forbidden_user = get_user_model().objects.create_user(**self.forbidden_user_credentials)
        self.author = get_user_model().objects.create_user(**self.author_credentials)
        self.new_taxonomy = Taxonomy.objects.create(
                title='test taxonomy',
                author=self.author,
                )
        self.url = reverse('taxonomies:update', kwargs={'slug_taxonomy': self.new_taxonomy.slug})
        # Login forbidden user
        self.client.post(reverse('login'), self.forbidden_user_credentials, follow=True)

    def test_page_status_code(self):
        response = self.client.get(f'/taxonomies/taxonomy/{self.new_taxonomy.slug}/update/')
        self.assertEqual(response.status_code, 403)

    def test_page_status_code_by_url_name(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 403)


class TaxonomyUpdateViewTestsAuthorAuthenticated(TestCase):

    def setUp(self):
        """ Create a user (for taxonomy) and taxonomy """
        self.credentials = {
                'username': 'newuser',
                'email': 'newuser@email.com',
                'password': 'secret',
                }
        self.new_user = get_user_model().objects.create_user(**self.credentials)
        self.new_taxonomy = Taxonomy.objects.create(
                title='test taxonomy',
                author=self.new_user,
                )
        self.url = reverse('taxonomies:update', kwargs={'slug_taxonomy': self.new_taxonomy.slug})
        # Login the author
        self.client.post(reverse('login'), self.credentials, follow=True)

    def test_page_status_code(self):
        response = self.client.get(f'/taxonomies/taxonomy/{self.new_taxonomy.slug}/update/')
        self.assertEqual(response.status_code, 200)

    def test_page_status_code_by_url_name(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_view_template(self):
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, 'taxonomy_update.html')


class TaxonomyDeleteteViewTestsNotAuthenticated(TestCase):

    def setUp(self):
        """ Create a user (for taxonomy) and taxonomy """
        self.credentials = {
                'username': 'newuser',
                'email': 'newuser@email.com',
                'password': 'secret',
                }
        self.new_user = get_user_model().objects.create_user(**self.credentials)
        self.new_taxonomy = Taxonomy.objects.create(
                title='test taxonomy',
                author=self.new_user,
                )
        self.url = reverse('taxonomies:delete', kwargs={'slug_taxonomy': self.new_taxonomy.slug})

    def test_page_status_code(self):
        response = self.client.get(f'/taxonomies/taxonomy/{self.new_taxonomy.slug}/delete/')
        self.assertEqual(response.status_code, 302)

    def test_page_status_code_by_url_name(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 302)

    def test_redirect(self):
        response = self.client.get(self.url)
        self.assertRedirects(response, f"{reverse('login')}?next={self.url}", target_status_code=200)


class TaxonomyDeleteViewTestsForbiddenUser(TestCase):

    def setUp(self):
        """ Create 2 users and a taxonomy """
        self.forbidden_user_credentials = {
                'username': 'forbidden_user',
                'email': 'forbidden_user@email.com',
                'password': 'secret',
                }
        self.author_credentials = {
                'username': 'author',
                'email': 'author@email.com',
                'password': 'secret',
                }
        self.forbidden_user = get_user_model().objects.create_user(**self.forbidden_user_credentials)
        self.author = get_user_model().objects.create_user(**self.author_credentials)
        self.new_taxonomy = Taxonomy.objects.create(
                title='test taxonomy',
                author=self.author,
                )
        self.url = reverse('taxonomies:delete', kwargs={'slug_taxonomy': self.new_taxonomy.slug})
        # Login forbidden user
        self.client.post(reverse('login'), self.forbidden_user_credentials, follow=True)

    def test_page_status_code(self):
        response = self.client.get(f'/taxonomies/taxonomy/{self.new_taxonomy.slug}/delete/')
        self.assertEqual(response.status_code, 403)

    def test_page_status_code_by_url_name(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 403)


class TaxonomyDeleteViewTestsAuthorAuthenticated(TestCase):

    def setUp(self):
        """ Create a user (for taxonomy) and taxonomy """
        self.credentials = {
                'username': 'newuser',
                'email': 'newuser@email.com',
                'password': 'secret',
                }
        self.new_user = get_user_model().objects.create_user(**self.credentials)
        self.new_taxonomy = Taxonomy.objects.create(
                title='test taxonomy',
                author=self.new_user,
                )
        self.url = reverse('taxonomies:delete', kwargs={'slug_taxonomy': self.new_taxonomy.slug})
        # Login the author
        self.client.post(reverse('login'), self.credentials, follow=True)

    def test_page_status_code(self):
        response = self.client.get(f'/taxonomies/taxonomy/{self.new_taxonomy.slug}/delete/')
        self.assertEqual(response.status_code, 200)

    def test_page_status_code_by_url_name(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_view_template(self):
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, 'taxonomy_confirm_delete.html')


class UserTaxonomyListViewTests(TestCase):

    def setUp(self):
        """ Create a user (for taxonomy) and taxonomy """
        self.credentials = {
                'username': 'newuser',
                'email': 'newuser@email.com',
                'password': 'secret',
                }
        self.new_user = get_user_model().objects.create_user(**self.credentials)
        self.new_taxonomy = Taxonomy.objects.create(
                title='test taxonomy',
                author=self.new_user,
                )
        self.url = reverse('taxonomies:user', kwargs={'username': self.new_user.username})

    def test_page_status_code(self):
        response = self.client.get(f'/taxonomies/{self.new_user.username}/')
        self.assertEqual(response.status_code, 200)

    def test_page_status_code_by_url_name(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_view_template(self):
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, 'user_taxonomy_list.html')


