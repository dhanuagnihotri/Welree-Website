from django.contrib.auth import get_user_model, logout
from django.core import mail
from django.db import IntegrityError

from welree.test_helpers import ExtendedTestCase
from welree import models

def create_and_login_user(self):
    model = get_user_model()
    users = model.objects.count()
    email = "user{}@example.com".format(users)
    response = self.post("/signup/", {"email": email, "password": "foobar", "first_name": "Charles", "last_name": "Atterly"})
    return model.objects.get(email=email)

class welreeApiTests(ExtendedTestCase):
    def setUp(self):
        ExtendedTestCase.setUp(self)
        self.persist_client()
        
    def test_login_logout(self):
        self.assertStatus(401, '/api/v1/user/logout/')
        self.assertStatus(405, '/api/v1/user/login/')
        response = self.api_post('/api/v1/user/login/', {}, raise_errors=False)
        self.assertEquals(response, {'success': False, 'reason': 'incorrect'})

        user = create_and_login_user(self)
        response = self.api_post('/api/v1/user/login/', {'username': user.username, 'password': 'foobar'}, raise_errors=False)
        self.assertEquals(response, {'success': True})
        response = self.api_get('/api/v1/user/logout/')
        self.assertEquals(response, {'success': True})

    def test_signup(self):
        self.assertStatus(405, '/api/v1/user/signup/')

        response = self.api_post('/api/v1/user/signup/', {}, raise_errors=False)
        self.assertEquals(response, {'success': False, 'reason':
            {'email': ['This field is required.'],
             'first_name': ['This field is required.'],
             'last_name': ['This field is required.'],
             'password': ['This field is required.']}
        })
        self.assertEqual(0, models.CustomUser.objects.count())

        response = self.api_post('/api/v1/user/signup/', {'email': 'foo@example.com', 'first_name': 'foo', 'last_name': 'bar', 'password': 'foobar'}, raise_errors=False)
        self.assertEqual(1, models.CustomUser.objects.count())

        response = self.api_post('/api/v1/user/signup/', {'email': 'foo@example.com', 'first_name': 'foo', 'last_name': 'bar', 'password': 'foobar'}, raise_errors=False)
        self.assertEquals(response, {'success': False, 'reason': {'email': ['This email address is already registered with Welree.']}})
        self.assertEqual(1, models.CustomUser.objects.count())

    def test_jewelrycollection_post(self):
        response = self.api_get('/api/v1/collection/')
        self.assertEquals(response['objects'], [])

        with self.assertRaises(ValueError):
            response = self.api_post('/api/v1/collection/', {}, raise_errors=False)

        user = create_and_login_user(self)
        response = self.api_post('/api/v1/collection/', {}, raise_errors=False)
        self.assertEquals(response, {'collection': {'kind': ['This field is required.'], 'name': ['This field is required.']}})

        response = self.api_post('/api/v1/collection/', { 'name': 'foo', 'kind': models.JewelryCollection.KIND_DESIGNER }, raise_errors=False)
        self.assertEquals(1, models.JewelryCollection.objects.count())
        self.assertEquals(response['id'], 1)

        response = self.api_post('/api/v1/collection/', { 'name': 'foo', 'kind': models.JewelryCollection.KIND_DESIGNER }, raise_errors=False)
        self.assertEquals(1, models.JewelryCollection.objects.count())
        self.assertEquals(response, {'collection': {'__all__': ['Jewelry collection with this Owner and Name already exists.']}})

    def test_jewelryitem_post(self):
        response = self.api_get('/api/v1/jewelry/')
        self.assertEquals(response['objects'], [])

        with self.assertRaises(ValueError):
            response = self.api_post('/api/v1/jewelry/', {}, raise_errors=False)

        user = create_and_login_user(self)
        response = self.api_post('/api/v1/jewelry/', {}, raise_errors=False)
        self.assertEquals(response, {'error': "The 'collection' field has no data and doesn't allow a default or null value."})

        self.assertEquals(0, models.JewelryItem.objects.count())
        collection = models.JewelryCollection.objects.create(owner=user, kind=models.JewelryCollection.KIND_DESIGNER, name='foo')
        response = self.api_post('/api/v1/jewelry/', {
            'collection': collection.id,
            'primary_photo': '/Users/mrooney/Desktop/passions.jpg',
            'description': 'foo'
        }, raise_errors=False)
        self.assertTrue(response['jewelry']['color'] == ['This field is required.'])
        self.assertEquals(0, models.JewelryItem.objects.count())

        response = self.api_post('/api/v1/jewelry/', {
            'collection': collection.id,
            'primary_photo': '/Users/mrooney/Desktop/passions.jpg',
            'description': 'foo',
            'color': 'foo', 'material': 'foo', 'type': 'foo', 'tags': 'foo',
        }, raise_errors=False)
        self.assertEquals(response['id'], 1)
        self.assertEquals(1, models.JewelryItem.objects.count())
        self.assertEquals(collection, models.JewelryItem.objects.all()[0].collection)

class welreeTests(ExtendedTestCase):
    def setUp(self):
        ExtendedTestCase.setUp(self)
        self.persist_client()
        
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

    def test_consumer_upload(self):
        self.assertStatus(301, '/consumer/upload')

        user = create_and_login_user(self)
        response = self.get('/consumer/upload/')
        self.assertTrue('form_ideabook_new' in response.context)
        self.assertTrue('form_jewelbox_new' in response.context)
        self.assertTrue('form_jewelryitem_new' in response.context)
        self.assertNumCssMatches(2, response, 'div.collection-new')
        self.assertNumCssMatches(1, response, 'div.ideabooks .collection-item')
        self.assertNumCssMatches(1, response, 'div.jewelboxes .collection-item')
        self.assertNumCssMatches(1, response, 'select#id_collection option')

        models.JewelryCollection.objects.create(owner=user, kind=models.JewelryCollection.KIND_IDEABOOK, name='foo')
        response = self.get('/consumer/upload/')
        self.assertNumCssMatches(2, response, 'div.ideabooks .collection-item')
        self.assertNumCssMatches(1, response, 'div.jewelboxes .collection-item')
        self.assertNumCssMatches(2, response, 'select#id_collection option')

        models.JewelryCollection.objects.create(owner=user, kind=models.JewelryCollection.KIND_JEWELBOX, name='foo2')
        response = self.get('/consumer/upload/')
        self.assertNumCssMatches(2, response, 'div.ideabooks .collection-item')
        self.assertNumCssMatches(2, response, 'div.jewelboxes .collection-item')
        self.assertNumCssMatches(3, response, 'select#id_collection option')

        # someone else's collection should not appear here!
        models.JewelryCollection.objects.create(owner_id=9, kind=models.JewelryCollection.KIND_IDEABOOK, name='foo3')
        response = self.get('/consumer/upload/')
        self.assertNumCssMatches(2, response, 'div.ideabooks .collection-item')
        self.assertNumCssMatches(3, response, 'select#id_collection option')

    def test_designer_upload(self):
        self.assertStatus(301, '/designer/upload')

        user = create_and_login_user(self)
        response = self.get('/designer/upload/')
        self.assertTrue('form_collection_new' in response.context)
        self.assertTrue('form_jewelryitem_new' in response.context)
        self.assertNumCssMatches(1, response, 'div.collection-new')

