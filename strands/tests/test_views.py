from django.test import TestCase

from django.urls import reverse

from django.contrib.auth import get_user_model
from curricula.models import Curriculum
from strands.models import Strand


class StrandCurriculumListPageViewTests(TestCase):
    """ List the strands of a curriclum """
    def setUp(self):
        """ Create a user (for curriculum) and curriculum """
        self.credentials = {
                'username': 'newuser',
                'email': 'newuser@email.com',
                'password': 'secret',
                }
        self.new_user = get_user_model().objects.create_user(**self.credentials)
        self.new_curriculum = Curriculum.objects.create(
                title='test curriculum',
                country='test country',
                author=self.new_user,
                )
        self.url = reverse('curricula:strands:list_curriculum', kwargs={'slug_curriculum': self.new_curriculum.slug, 'pk_curriculum': self.new_curriculum.pk})


    def test_page_status_code(self):
        response = self.client.get(f'/curricula/curriculum/{self.new_curriculum.slug}/strands/{self.new_curriculum.pk}/strands/')
        self.assertEqual(response.status_code, 200)

    def test_page_status_code_by_url_name(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_view_template(self):
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, 'strand_list.html')


class StrandCreatePageViewTestsNotAuthenticated(TestCase):
    """ Should be redirected to 'login' when unauthenticated user tries to create """

    def setUp(self):
        """ Create a user (for curriculum) and curriculum """
        self.credentials = {
                'username': 'newuser',
                'email': 'newuser@email.com',
                'password': 'secret',
                }
        self.new_user = get_user_model().objects.create_user(**self.credentials)
        self.new_curriculum = Curriculum.objects.create(
                title='test curriculum',
                country='test country',
                author=self.new_user,
                )
        self.url = reverse('curricula:strands:create', kwargs={'slug_curriculum': self.new_curriculum.slug, 'pk_curriculum': self.new_curriculum.pk})


    def test_page_status_code(self):
        response = self.client.get(f'/curricula/curriculum/{self.new_curriculum.slug}/strands/{self.new_curriculum.pk}/strand/new/')
        self.assertEqual(response.status_code, 302)

    def test_page_status_code_by_url_name(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 302)

    def test_redirect(self):
        response = self.client.get(self.url)
        self.assertRedirects(response, f"{reverse('login')}?next={self.url}", target_status_code=200)

class StrandCreatePageViewTestsForbiddenUser(TestCase):
    """ For an authenticated user who is not the author of the curriculum """
    def setUp(self):
        """ Create a user (author curriculum) and curriculum """
        self.credentials_author = {
                'username': 'newuser',
                'email': 'newuser@email.com',
                'password': 'secret',
                }
        self.user_author = get_user_model().objects.create_user(**self.credentials_author)
        self.new_curriculum = Curriculum.objects.create(
                title='test curriculum',
                country='test country',
                author=self.user_author,
                )
        # A non-author user
        self.credentials_forbidden = {
                'username': 'forbiddenUser',
                'email': 'forbidden@email.com',
                'password': 'secret',
                }
        self.user_forbidden = get_user_model().objects.create_user(**self.credentials_forbidden)
        self.url = reverse('curricula:strands:create', kwargs={'slug_curriculum': self.new_curriculum.slug, 'pk_curriculum': self.new_curriculum.pk})
        # Login the forbidden user
        self.client.post(reverse('login'), self.credentials_forbidden, follow=True)

    def test_page_status_code(self):
        response = self.client.get(f'/curricula/curriculum/{self.new_curriculum.slug}/strands/{self.new_curriculum.pk}/strand/new/')
        self.assertEqual(response.status_code, 403)

    def test_page_status_code_by_url_name(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 403)


class StrandCreatePageViewTestsCurriculumAuthor(TestCase):
    """ When the author of a curriculum tries to create a strand """

    def setUp(self):
        """ Create a user (for curriculum) and curriculum """
        self.credentials = {
                'username': 'newuser',
                'email': 'newuser@email.com',
                'password': 'secret',
                }
        self.new_user = get_user_model().objects.create_user(**self.credentials)
        self.new_curriculum = Curriculum.objects.create(
                title='test curriculum',
                country='test country',
                author=self.new_user,
                )
        self.url = reverse('curricula:strands:create', kwargs={'slug_curriculum': self.new_curriculum.slug, 'pk_curriculum': self.new_curriculum.pk})
        # Login the author user
        self.client.post(reverse('login'), self.credentials, follow=True)

    def test_page_status_code(self):
        response = self.client.get(f'/curricula/curriculum/{self.new_curriculum.slug}/strands/{self.new_curriculum.pk}/strand/new/')
        self.assertEqual(response.status_code, 200)

    def test_page_status_code_by_url_name(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_view_template(self):
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, 'strand_form.html')


class StrandDetailPageViewTests(TestCase):

    def setUp(self):
        """ Create a user, curriculum and strand """
        self.credentials = {
                'username': 'newuser',
                'email': 'newuser@email.com',
                'password': 'secret',
                }
        self.new_user = get_user_model().objects.create_user(**self.credentials)
        self.new_curriculum = Curriculum.objects.create(
                title='test curriculum',
                country='test country',
                author=self.new_user,
                )
        self.new_strand = Strand.objects.create(
                title='test strand',
                curriculum=self.new_curriculum,
                )
        self.url = reverse('curricula:strands:detail', kwargs={'slug_curriculum': self.new_curriculum.slug, 'pk_curriculum': self.new_curriculum.pk, 'slug_strand': self.new_strand.slug})

    def test_page_status_code(self):
        response = self.client.get(f'/curricula/curriculum/{self.new_curriculum.slug}/strands/{self.new_curriculum.pk}/strand/{self.new_strand.slug}/')
        self.assertEqual(response.status_code, 200)

    def test_page_status_code_by_url_name(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_view_template(self):
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, 'strand_detail.html')


class StrandUpdatePageViewTestsNotAuthenticated(TestCase):
    """ Should be redirected to 'login' when unauthenticated user tries to update """

    def setUp(self):
        """ Create a user, curriculum and strand """
        self.credentials = {
                'username': 'newuser',
                'email': 'newuser@email.com',
                'password': 'secret',
                }
        self.new_user = get_user_model().objects.create_user(**self.credentials)
        self.new_curriculum = Curriculum.objects.create(
                title='test curriculum',
                country='test country',
                author=self.new_user,
                )
        self.new_strand = Strand.objects.create(
                title='test strand',
                curriculum=self.new_curriculum,
                )
        self.url = reverse('curricula:strands:update', kwargs={'slug_curriculum': self.new_curriculum.slug, 'pk_curriculum': self.new_curriculum.pk, 'slug_strand': self.new_strand.slug})

    def test_page_status_code(self):
        response = self.client.get(f'/curricula/curriculum/{self.new_curriculum.slug}/strands/{self.new_curriculum.pk}/strand/{self.new_strand.slug}/update/')
        self.assertEqual(response.status_code, 302)

    def test_page_status_code_by_url_name(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 302)

    def test_redirect(self):
        response = self.client.get(self.url)
        self.assertRedirects(response, f"{reverse('login')}?next={self.url}", target_status_code=200)

class StrandUpdatePageViewTestsForbiddenUser(TestCase):
    """ For an authenticated user who is not the author of the strand/curriculum """
    def setUp(self):
        """ Create a user (author curriculum) and curriculum """
        self.credentials_author = {
                'username': 'newuser',
                'email': 'newuser@email.com',
                'password': 'secret',
                }
        self.user_author = get_user_model().objects.create_user(**self.credentials_author)
        self.new_curriculum = Curriculum.objects.create(
                title='test curriculum',
                country='test country',
                author=self.user_author,
                )
        self.new_strand = Strand.objects.create(
                title='test strand',
                curriculum=self.new_curriculum,
                )
        # A non-author user
        self.credentials_forbidden = {
                'username': 'forbiddenUser',
                'email': 'forbidden@email.com',
                'password': 'secret',
                }
        self.user_forbidden = get_user_model().objects.create_user(**self.credentials_forbidden)
        # Login the forbidden user
        self.client.post(reverse('login'), self.credentials_forbidden, follow=True)

        self.url = reverse('curricula:strands:update', kwargs={'slug_curriculum': self.new_curriculum.slug, 'pk_curriculum': self.new_curriculum.pk, 'slug_strand': self.new_strand.slug})

    def test_page_status_code(self):
        response = self.client.get(f'/curricula/curriculum/{self.new_curriculum.slug}/strands/{self.new_curriculum.pk}/strand/{self.new_strand.slug}/update/')
        self.assertEqual(response.status_code, 403)

    def test_page_status_code_by_url_name(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 403)


class StrandUpdatePageViewTestsStrandAuthor(TestCase):
    """ When the author of the strand tries to update """

    def setUp(self):
        """ Create a user, curriculum and strand """
        self.credentials = {
                'username': 'newuser',
                'email': 'newuser@email.com',
                'password': 'secret',
                }
        self.new_user = get_user_model().objects.create_user(**self.credentials)
        self.new_curriculum = Curriculum.objects.create(
                title='test curriculum',
                country='test country',
                author=self.new_user,
                )
        self.new_strand = Strand.objects.create(
                title='test strand',
                curriculum=self.new_curriculum,
                )
        self.url = reverse('curricula:strands:update', kwargs={'slug_curriculum': self.new_curriculum.slug, 'pk_curriculum': self.new_curriculum.pk, 'slug_strand': self.new_strand.slug})
        # Login the author
        self.client.post(reverse('login'), self.credentials, follow=True)

    def test_page_status_code(self):
        response = self.client.get(f'/curricula/curriculum/{self.new_curriculum.slug}/strands/{self.new_curriculum.pk}/strand/{self.new_strand.slug}/update/')
        self.assertEqual(response.status_code, 200)

    def test_page_status_code_by_url_name(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_view_template(self):
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, 'strand_update.html')


class StrandDeletePageViewTestsNotAuthenticated(TestCase):
    """ Should be redirected to 'login' when unauthenticated user tries to update """

    def setUp(self):
        """ Create a user, curriculum and strand """
        self.credentials = {
                'username': 'newuser',
                'email': 'newuser@email.com',
                'password': 'secret',
                }
        self.new_user = get_user_model().objects.create_user(**self.credentials)
        self.new_curriculum = Curriculum.objects.create(
                title='test curriculum',
                country='test country',
                author=self.new_user,
                )
        self.new_strand = Strand.objects.create(
                title='test strand',
                curriculum=self.new_curriculum,
                )
        self.url = reverse('curricula:strands:delete', kwargs={'slug_curriculum': self.new_curriculum.slug, 'pk_curriculum': self.new_curriculum.pk, 'slug_strand': self.new_strand.slug})

    def test_page_status_code(self):
        response = self.client.get(f'/curricula/curriculum/{self.new_curriculum.slug}/strands/{self.new_curriculum.pk}/strand/{self.new_strand.slug}/delete/')
        self.assertEqual(response.status_code, 302)

    def test_page_status_code_by_url_name(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 302)

    def test_redirect(self):
        response = self.client.get(self.url)
        self.assertRedirects(response, f"{reverse('login')}?next={self.url}", target_status_code=200)

class StrandDeletePageViewTestsForbiddenUser(TestCase):
    """ For an authenticated user who is not the author of the strand/curriculum """
    def setUp(self):
        """ Create a user (author curriculum) and curriculum """
        self.credentials_author = {
                'username': 'newuser',
                'email': 'newuser@email.com',
                'password': 'secret',
                }
        self.user_author = get_user_model().objects.create_user(**self.credentials_author)
        self.new_curriculum = Curriculum.objects.create(
                title='test curriculum',
                country='test country',
                author=self.user_author,
                )
        self.new_strand = Strand.objects.create(
                title='test strand',
                curriculum=self.new_curriculum,
                )
        # A non-author user
        self.credentials_forbidden = {
                'username': 'forbiddenUser',
                'email': 'forbidden@email.com',
                'password': 'secret',
                }
        self.user_forbidden = get_user_model().objects.create_user(**self.credentials_forbidden)
        # Login the forbidden user
        self.client.post(reverse('login'), self.credentials_forbidden, follow=True)

        self.url = reverse('curricula:strands:delete', kwargs={'slug_curriculum': self.new_curriculum.slug, 'pk_curriculum': self.new_curriculum.pk, 'slug_strand': self.new_strand.slug})

    def test_page_status_code(self):
        response = self.client.get(f'/curricula/curriculum/{self.new_curriculum.slug}/strands/{self.new_curriculum.pk}/strand/{self.new_strand.slug}/delete/')
        self.assertEqual(response.status_code, 403)

    def test_page_status_code_by_url_name(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 403)


class StrandDeletePageViewTestsStrandAuthor(TestCase):
    """ When the author of the strand tries to Delete """

    def setUp(self):
        """ Create a user, curriculum and strand """
        self.credentials = {
                'username': 'newuser',
                'email': 'newuser@email.com',
                'password': 'secret',
                }
        self.new_user = get_user_model().objects.create_user(**self.credentials)
        self.new_curriculum = Curriculum.objects.create(
                title='test curriculum',
                country='test country',
                author=self.new_user,
                )
        self.new_strand = Strand.objects.create(
                title='test strand',
                curriculum=self.new_curriculum,
                )
        self.url = reverse('curricula:strands:delete', kwargs={'slug_curriculum': self.new_curriculum.slug, 'pk_curriculum': self.new_curriculum.pk, 'slug_strand': self.new_strand.slug})
        # Login the author
        self.client.post(reverse('login'), self.credentials, follow=True)

    def test_page_status_code(self):
        response = self.client.get(f'/curricula/curriculum/{self.new_curriculum.slug}/strands/{self.new_curriculum.pk}/strand/{self.new_strand.slug}/delete/')
        self.assertEqual(response.status_code, 200)

    def test_page_status_code_by_url_name(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_view_template(self):
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, 'strand_confirm_delete.html')

