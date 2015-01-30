from django.contrib.auth import get_user_model

from welree.test_helpers import ExtendedTestCase
from welree import models

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
        self.assertStatus(200, '/signup/')
        user = self.signup_user()
        self.assertEqual(1, user.id)

    def test_password_reset(self):
        self.assertStatus(200, '/password_reset')

