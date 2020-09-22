from django.test import SimpleTestCase, TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from accounts.models import CustomUser, Profile


class SignUpViewTests(SimpleTestCase):

    def test_page_status_code(self):
        response = self.client.get('/accounts/signup/')
        self.assertEqual(response.status_code, 200)

    def test_page_status_code_by_url_name(self):
        response = self.client.get(reverse('signup'))
        self.assertEqual(response.status_code, 200)

    def test_view_template(self):
        response = self.client.get(reverse('signup'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'signup.html')


class LoginViewTests(SimpleTestCase):

    def test_page_status_code(self):
        response = self.client.get('/accounts/login/')
        self.assertEqual(response.status_code, 200)

    def test_view_url_by_name(self):
        response = self.client.get(reverse('login'))
        self.assertEqual(response.status_code, 200)

    def test_view_template(self):
        response = self.client.get(reverse('login'))
        self.assertTemplateUsed(response, 'registration/login.html')


class LogoutViewTestsNotAuthenticated(SimpleTestCase):

    def test_page_status_code(self):
        response = self.client.get('/accounts/logout/')
        self.assertEqual(response.status_code, 302)

    def test_view_url_by_name(self):
        response = self.client.get(reverse('logout'))
        self.assertEqual(response.status_code, 302)

    def test_redirect(self):
        response = self.client.get(reverse('logout'))
        self.assertRedirects(response, f"{reverse('pages:home')}", target_status_code=200)


class LoginTest(TestCase):

    def setUp(self):
        """ Create a user to test the login """
        self.credentials = {
                'username': 'newuser',
                'email': 'newuser@email.com',
                'password': 'secret',
                }
        self.new_user = get_user_model().objects.create_user(**self.credentials)

    def test_login(self):
        response = self.client.post(reverse('login'), self.credentials, follow=True)
        self.assertTrue(response.context['user'].is_authenticated)


class LogoutViewTestsAuthenticated(TestCase):

    def setUp(self):
        """ Create a user to test the logout page, user gets redirected to home """
        self.credentials = {
                'username': 'newuser',
                'email': 'newuser@email.com',
                'password': 'secret',
                }
        self.new_user = get_user_model().objects.create_user(**self.credentials)
        self.client.post(reverse('login'), self.credentials, follow=True)


    def test_page_status_code(self):
        response = self.client.get('/accounts/logout/')
        self.assertEqual(response.status_code, 302)

    def test_view_url_by_name(self):
        response = self.client.get(reverse('logout'))
        self.assertEqual(response.status_code, 302)

    def test_redirect(self):
        response = self.client.get(reverse('logout'))
        self.assertRedirects(response, f"{reverse('pages:home')}", target_status_code=200)


class ProfileViewTestsAuthenticated(TestCase):

    def setUp(self):
        """ Create a user to test the profile page, post_save signal is sent for profile creation"""
        self.credentials = {
                'username': 'newuser',
                'email': 'newuser@email.com',
                'password': 'secret',
                }
        self.new_user = get_user_model().objects.create_user(**self.credentials)
        self.profile_url = reverse('profile')
        self.client.post(reverse('login'), self.credentials, follow=True)

    def test_page_status_code(self):
        response = self.client.get('/accounts/profile/')
        self.assertEqual(response.status_code, 200)

    def test_page_status_code_by_url_name(self):
        response = self.client.get(self.profile_url)
        self.assertEqual(response.status_code, 200)

    def test_view_template(self):
        response = self.client.get(self.profile_url)
        self.assertTemplateUsed(response, 'profile.html')

    def test_profile_content(self):
        response = self.client.get(self.profile_url)
        self.assertContains(response, self.new_user.username)
        self.assertContains(response, self.new_user.email)


class PasswordChangeViewTestsNotAuthenticated(SimpleTestCase):
    """ We expect to be redirected to 'login' in this case """

    def test_page_status_code(self):
        response = self.client.get('/accounts/password_change/')
        self.assertEqual(response.status_code, 302)

    def test_page_status_code_by_url_name(self):
        response = self.client.get(reverse('password_change'))
        self.assertEqual(response.status_code, 302)

    def test_redirect(self):
        response = self.client.get(reverse('password_change'))
        self.assertRedirects(response, f"{reverse('login')}?next={reverse('password_change')}", target_status_code=200)


class PasswordChangeViewTestsAuthenticated(TestCase):

    def setUp(self):
        """ Create a user to test the password change view"""
        self.credentials = {
                'username': 'newuser',
                'email': 'newuser@email.com',
                'password': 'secret',
                }
        self.new_user = get_user_model().objects.create_user(**self.credentials)
        self.password_change_url = reverse('password_change')
        self.client.post(reverse('login'), self.credentials, follow=True)

    def test_page_status_code(self):
        response = self.client.get('/accounts/password_change/')
        self.assertEqual(response.status_code, 200)

    def test_page_status_code_by_url_name(self):
        response = self.client.get(reverse('password_change'))
        self.assertEqual(response.status_code, 200)

    def test_view_template(self):
        response = self.client.get(reverse('password_change'))
        self.assertTemplateUsed(response, 'registration/password_change_form.html')


class PasswordChangeDoneViewTestsNotAuthenticated(SimpleTestCase):
    """ We expect to be redirected to 'login' in this case """

    def test_page_status_code(self):
        response = self.client.get('/accounts/password_change/done')
        self.assertEqual(response.status_code, 301) # Get a 301 moved permanently status code instead of 302
        # Not sure exactly why

    def test_page_status_code_by_url_name(self):
        response = self.client.get(reverse('password_change_done'))
        self.assertEqual(response.status_code, 302)

    def test_redirect(self):
        response = self.client.get(reverse('password_change_done'))
        self.assertRedirects(response, f"{reverse('login')}?next={reverse('password_change_done')}", target_status_code=200)


class PasswordChangeDoneViewTestsAuthenticated(TestCase):

    def setUp(self):
        """ Create a user to test the password change view"""
        self.credentials = {
                'username': 'newuser',
                'email': 'newuser@email.com',
                'password': 'secret',
                }
        self.new_user = get_user_model().objects.create_user(**self.credentials)
        self.client.post(reverse('login'), self.credentials, follow=True)


    def test_page_status_code_by_url_name(self):
        response = self.client.get(reverse('password_change_done'))
        self.assertEqual(response.status_code, 200)

    def test_view_template(self):
        response = self.client.get(reverse('password_change_done'))
        self.assertTemplateUsed(response, 'registration/password_change_done.html')


class PasswordChangeViewTestsAuthenticated(TestCase):

    def setUp(self):
        """ Create a user to test the password change view"""
        self.credentials = {
                'username': 'newuser',
                'email': 'newuser@email.com',
                'password': 'secret',
                }
        self.new_user = get_user_model().objects.create_user(**self.credentials)
        self.password_change_url = reverse('password_change')
        self.client.post(reverse('login'), self.credentials, follow=True)

    def test_page_status_code(self):
        response = self.client.get('/accounts/password_change/')
        self.assertEqual(response.status_code, 200)

    def test_page_status_code_by_url_name(self):
        response = self.client.get(reverse('password_change'))
        self.assertEqual(response.status_code, 200)

    def test_view_template(self):
        response = self.client.get(reverse('password_change'))
        self.assertTemplateUsed(response, 'registration/password_change_form.html')


class PasswordResetViewTests(SimpleTestCase):
    """ Reset applies to non-authenticated users but can also be used by authenticated ones  """

    def test_page_status_code(self):
        response = self.client.get('/accounts/password_reset/')
        self.assertEqual(response.status_code, 200)

    def test_page_status_code_by_url_name(self):
        response = self.client.get(reverse('password_reset'))
        self.assertEqual(response.status_code, 200)

    def test_view_template(self):
        response = self.client.get(reverse('password_reset'))
        self.assertTemplateUsed(response, 'registration/password_reset_form.html')


class PasswordResetDoneViewTests(SimpleTestCase):
    """ Applies to non-authenticated users but can also be used by authenticated ones  """

    def test_page_status_code(self):
        response = self.client.get('/accounts/password_reset/done/')
        self.assertEqual(response.status_code, 200)

    def test_page_status_code_by_url_name(self):
        response = self.client.get(reverse('password_reset_done'))
        self.assertEqual(response.status_code, 200)

    def test_view_template(self):
        response = self.client.get(reverse('password_reset_done'))
        self.assertTemplateUsed(response, 'registration/password_reset_done.html')


class PasswordResetConfirmViewTests(TestCase):
    """ Applies to non-authenticated users but can also be used by authenticated ones  """

    #### Need to sort out tokens for testing reset confirm! ##

    #def test_page_status_code(self):
    #    response = self.client.get('/accounts/reset/MQ/set-password/')
    #    self.assertEqual(response.status_code, 200)

    #def test_page_status_code_by_url_name(self):
    #    response = self.client.get(reverse('password_reset_confirm'))
    #    self.assertEqual(response.status_code, 200)

    #def test_view_template(self):
    #    response = self.client.get(reverse('password_reset_confirm'))
    #    self.assertTemplateUsed(response, 'registration/password_reset_confirm.html')


class PasswordResetCompleteViewTests(SimpleTestCase):
    """ Applies to non-authenticated users but can also be used by authenticated ones  """

    def test_page_status_code(self):
        response = self.client.get('/accounts/reset/done/')
        self.assertEqual(response.status_code, 200)

    def test_page_status_code_by_url_name(self):
        response = self.client.get(reverse('password_reset_complete'))
        self.assertEqual(response.status_code, 200)

    def test_view_template(self):
        response = self.client.get(reverse('password_reset_complete'))
        self.assertTemplateUsed(response, 'registration/password_reset_complete.html')


