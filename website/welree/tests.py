from django.contrib.auth import get_user_model
from django.core import mail

from welree.test_helpers import ExtendedTestCase
from welree import models

class welreeApiTests(ExtendedTestCase):
    def test_login_logout(self):
        self.assertStatus(401, '/api/v1/user/logout/?format=json')
        self.assertStatus(405, '/api/v1/user/login/?format=json')
        response = self.api_post('/api/v1/user/login/', {}, raise_errors=False)
        self.assertEquals(response, {'success': False, 'reason': 'incorrect'})

class welreeTests(ExtendedTestCase):
    def signup_user(self):
        model = get_user_model()
        users = model.objects.count()
        self.post("/signup/", {"email": "user{}@example.com".format(users), "password": "foobar"})
        return model.objects.get(id=users+1)

    def test_404(self):
        self.assertStatus(404, '/foobar/')

    def test_home(self):
        self.assertStatus(200, '/')

    def test_login(self):
        self.assertStatus(200, '/login/')

    def test_logout(self):
        response = self.get('/logout/')
        self.assertRedirects(response, '/')

    def test_signup(self):
        response = self.get('/signup/')
        self.assertTrue('signup_form' in response.context)
        self.assertFalse(response.context['signup_form'].errors)
        data = response.context['signup_form'].data
        data['email'] = 'foo@rowk'
        data['password'] = 'foobar'
        data['first_name'] = 'Charles'
        data['last_name'] = 'Atterly'
        response = self.post('/signup/', data=data)

        self.assertEqual(0, models.CustomUser.objects.count())
        self.assertTrue('email' in response.context['signup_form'].errors)
        self.assertEqual(len(mail.outbox), 0)

        data['email'] = 'foo@rowk.com'
        response = self.post('/signup/', data=data)
        self.assertEqual(1, models.CustomUser.objects.count())
        self.assertEqual(len(mail.outbox), 1)
        self.assertItemsEqual(mail.outbox[0].recipients(), ['foo@rowk.com'])

        # Test a duplicate email
        response = self.post('/signup/', data=data)
        self.assertTrue('email' in response.context['signup_form'].errors)
        self.assertEqual(1, models.CustomUser.objects.count())

    def test_password_reset(self):
        self.assertStatus(200, '/password_reset')

