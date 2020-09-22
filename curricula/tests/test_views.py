from django.test import TestCase

from django.urls import reverse

from django.contrib.auth import get_user_model
from curricula.models import Curriculum


class CurriculumHomePageViewTests(TestCase):

    def test_page_status_code(self):
        response = self.client.get('/curricula/')
        self.assertEqual(response.status_code, 200)

    def test_page_status_code_by_url_name(self):
        response = self.client.get(reverse('curricula:home'))
        self.assertEqual(response.status_code, 200)

    def test_view_template(self):
        response = self.client.get(reverse('curricula:home'))
        self.assertTemplateUsed(response, 'curriculum_list.html')


class CurriculumUserListPageViewTests(TestCase):

    def setUp(self):
        """ Create a user to test the user list """
        self.credentials = {
                'username': 'newuser',
                'email': 'newuser@email.com',
                'password': 'secret',
                }
        self.new_user = get_user_model().objects.create_user(**self.credentials)
        self.user_list_url = reverse('curricula:user', kwargs={'username': self.new_user.username})
        self.client.post(reverse('login'), self.credentials, follow=True)

    def test_page_status_code(self):
        response = self.client.get(f"/curricula/{self.new_user.username}/")
        self.assertEqual(response.status_code, 200)

    def test_page_status_code_by_url_name(self):
        response = self.client.get(self.user_list_url)
        self.assertEqual(response.status_code, 200)

    def test_view_template(self):
        response = self.client.get(self.user_list_url)
        self.assertTemplateUsed(response, 'user_curriculum_list.html')


class CurriculumCreatePageViewTestsNotAuthenticated(TestCase):
    """ Should be redirected to 'login' when unauthenticated user tries to create """

    def test_page_status_code(self):
        response = self.client.get('/curricula/curriculum/new/')
        self.assertEqual(response.status_code, 302)

    def test_page_status_code_by_url_name(self):
        response = self.client.get(reverse('curricula:create'))
        self.assertEqual(response.status_code, 302)

    def test_redirect(self):
        response = self.client.get(reverse('curricula:create'))
        self.assertRedirects(response, f"{reverse('login')}?next={reverse('curricula:create')}", target_status_code=200)


class CurriculumCreatePageViewTestsAuthenticated(TestCase):

    def setUp(self):
        """ Create a user to test the user list """
        self.credentials = {
                'username': 'newuser',
                'email': 'newuser@email.com',
                'password': 'secret',
                }
        self.new_user = get_user_model().objects.create_user(**self.credentials)
        self.client.post(reverse('login'), self.credentials, follow=True)

    def test_page_status_code(self):
        response = self.client.get('/curricula/curriculum/new/')
        self.assertEqual(response.status_code, 200)

    def test_page_status_code_by_url_name(self):
        response = self.client.get(reverse('curricula:create'))
        self.assertEqual(response.status_code, 200)

    def test_view_template(self):
        response = self.client.get(reverse('curricula:create'))
        self.assertTemplateUsed(response, 'curriculum_form.html')


class CurriculumDetailPageViewTests(TestCase):

    def setUp(self):
        """ Create a user and curriculum """
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
        self.curriculum_url = reverse('curricula:detail', kwargs={'slug_curriculum': self.new_curriculum.slug})

    def test_page_status_code(self):
        response = self.client.get(f"/curricula/curriculum/{self.new_curriculum.slug}/")
        self.assertEqual(response.status_code, 200)

    def test_page_status_code_by_url_name(self):
        response = self.client.get(self.curriculum_url)
        self.assertEqual(response.status_code, 200)

    def test_view_template(self):
        response = self.client.get(self.curriculum_url)
        self.assertTemplateUsed(response, 'curriculum_detail.html')


class CurriculumUpdatePageViewTestsNotAuthenticated(TestCase):
    """ Should be redirected to 'login' when unauthenticated user tries to update """
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
        self.url = reverse('curricula:update', kwargs={'slug_curriculum': self.new_curriculum.slug})


    def test_page_status_code(self):
        response = self.client.get(f'/curricula/curriculum/{self.new_curriculum.slug}/update/')
        self.assertEqual(response.status_code, 302)

    def test_page_status_code_by_url_name(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 302)

    def test_redirect(self):
        response = self.client.get(self.url)
        self.assertRedirects(response, f"{reverse('login')}?next={self.url}", target_status_code=200)


class CurriculumUpdatePageViewTestsForbiddenUser(TestCase):
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
        self.url = reverse('curricula:update', kwargs={'slug_curriculum': self.new_curriculum.slug})
        # Login the forbidden user
        self.client.post(reverse('login'), self.credentials_forbidden, follow=True)

    def test_page_status_code(self):
        response = self.client.get(f'/curricula/curriculum/{self.new_curriculum.slug}/update/')
        self.assertEqual(response.status_code, 403)

    def test_page_status_code_by_url_name(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 403)


class CurriculumUpdatePageViewTestsCurriculumAuthor(TestCase):
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
        self.url = reverse('curricula:update', kwargs={'slug_curriculum': self.new_curriculum.slug})
        # Login the author of curriculum
        self.client.post(reverse('login'), self.credentials, follow=True)

    def test_page_status_code(self):
        response = self.client.get(f'/curricula/curriculum/{self.new_curriculum.slug}/update/')
        self.assertEqual(response.status_code, 200)

    def test_page_status_code_by_url_name(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_view_template(self):
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, 'curriculum_update.html')


class CurriculumDeletePageViewTestsNotAuthenticated(TestCase):
    """ Should be redirected to 'login' when unauthenticated user tries to delete """
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
        self.url = reverse('curricula:delete', kwargs={'slug_curriculum': self.new_curriculum.slug})


    def test_page_status_code(self):
        response = self.client.get(f'/curricula/curriculum/{self.new_curriculum.slug}/delete/')
        self.assertEqual(response.status_code, 302)

    def test_page_status_code_by_url_name(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 302)

    def test_redirect(self):
        response = self.client.get(self.url)
        self.assertRedirects(response, f"{reverse('login')}?next={self.url}", target_status_code=200)


class CurriculumDeletePageViewTestsForbiddenUser(TestCase):
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
        self.url = reverse('curricula:delete', kwargs={'slug_curriculum': self.new_curriculum.slug})
        # Login the forbidden user
        self.client.post(reverse('login'), self.credentials_forbidden, follow=True)

    def test_page_status_code(self):
        response = self.client.get(f'/curricula/curriculum/{self.new_curriculum.slug}/delete/')
        self.assertEqual(response.status_code, 403)

    def test_page_status_code_by_url_name(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 403)


class CurriculumDeletePageViewTestsCurriculumAuthor(TestCase):
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
        self.url = reverse('curricula:delete', kwargs={'slug_curriculum': self.new_curriculum.slug})
        # Login the author of curriculum
        self.client.post(reverse('login'), self.credentials, follow=True)

    def test_page_status_code(self):
        response = self.client.get(f'/curricula/curriculum/{self.new_curriculum.slug}/delete/')
        self.assertEqual(response.status_code, 200)

    def test_page_status_code_by_url_name(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_view_template(self):
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, 'curriculum_confirm_delete.html')


