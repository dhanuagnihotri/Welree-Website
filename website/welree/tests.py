from django.contrib.auth import get_user_model, logout
from django.core import mail
from django.db import IntegrityError

from welree.test_helpers import ExtendedTestCase
from welree import models

DEFAULT_TEST_IMAGE = 'jewelry/10892026_10101402515514571_743122767897543427_n.jpg'

def create_and_login_user(self, **kwargs):
    model = get_user_model()
    users = model.objects.count()
    email = "user{}@example.com".format(users)
    data = {"email": email, "password": "foobar", "first_name": "Charles", "last_name": "Atterly"}
    data.update(kwargs)
    response = self.post("/signup/", data)
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
        self.assertEquals(0, models.JewelryItem.objects.count())
        collection = models.JewelryCollection.objects.create(owner=user, kind=models.JewelryCollection.KIND_DESIGNER, name='foo')
        collection2 = models.JewelryCollection.objects.create(owner=user, kind=models.JewelryCollection.KIND_DESIGNER, name='bar')
        response = self.api_post('/api/v1/jewelry/', {
            'primary_photo': DEFAULT_TEST_IMAGE,
            'description': 'foo'
        }, raise_errors=False)
        self.assertTrue(response['jewelry']['color'] == ['This field is required.'])
        self.assertEquals(0, models.JewelryItem.objects.count())

        response = self.api_post('/api/v1/jewelry/', {
            'primary_photo': '/Users/mrooney/Desktop/passions.jpg',
            'description': 'foo',
            'color': 'foo', 'material': 'foo', 'type': 'foo',
            'collection': collection.id,
        }, raise_errors=False)
        self.assertEquals(response['id'], 1)
        self.assertEquals(1, models.JewelryItem.objects.count())
        self.assertEquals(list(collection.items.all()), [models.JewelryItem.objects.first()])
        self.assertEquals(list(collection2.items.all()), [])
        response = self.api_post('/api/v1/collection/add/', {
            'item': response['id'],
            'collection': collection2.id,
        }, raise_errors=False)
        self.assertEquals(response, {'redirect': '/collection/2/bar/', 'success': True})
        self.assertEquals(list(collection2.items.all()), [models.JewelryItem.objects.first()])

class welreeTests(ExtendedTestCase):
    def setUp(self):
        ExtendedTestCase.setUp(self)
        self.persist_client()

    def createItem(self, owner, collection=None, **kwargs):
        defaults = {
                'description': 'description',
                'url': 'http://www.example.com/foobar/',
                'material': 'Wood',
                'color': 'Black',
                'type': 'Earring',
                'primary_photo': DEFAULT_TEST_IMAGE,
        }
        defaults.update(kwargs)
        item = models.JewelryItem.objects.create(owner=owner, **defaults)
        collection = collection or models.JewelryCollection.objects.get_or_create(owner=owner, kind=models.JewelryCollection.KIND_JEWELBOX, name='My Collection {}'.format(models.JewelryCollection.objects.count()))[0]
        collection.items.add(item)
        return item

    def test_404(self):
        self.assertStatus(404, '/foobar/')

    def test_user_properties(self):
        user = create_and_login_user(self)

        self.assertEquals(user.noun, "User")

        user.is_designer = True
        self.assertEquals(user.noun, "Designer")

    def test_admin_designeritem(self):
        user = create_and_login_user(self)
        user.is_staff = True
        user.is_superuser = True
        user.save()

        self.get('/admin/welree/designeritem/')

    def test_settings(self):
        self.assertStatus(302, '/settings/')
        create_and_login_user(self)
        self.assertStatus(200, '/settings/')

    def test_home(self):
        self.assertStatus(200, '/')

        user = create_and_login_user(self)
        collection = models.JewelryCollection.objects.create(owner=user, kind=models.JewelryCollection.KIND_DESIGNER, name='a')
        item = self.createItem(owner=user, collection=collection, is_approved=True)
        response = self.get('/')
        self.assertNumCssMatches(0, response, '#top-carousel ol.carousel-indicators li')
        self.assertNumCssMatches(1, response, '#top-carousel div.item')

    def test_login(self):
        self.assertStatus(200, '/login/')

    def test_logout(self):
        response = self.get('/logout/')
        self.assertRedirects(response, '/')

    def test_search(self):
        response = self.get('/search/all/?q=foo')
        self.assertTrue("<h2>No results matched your search.</h2>" in response.content)

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

        user = create_and_login_user(self, is_designer=True)
        response = self.get('/designer/upload/')
        self.assertTrue('form_collection_new' in response.context)
        self.assertTrue('form_jewelryitem_new' in response.context)
        self.assertNumCssMatches(1, response, 'div.collection-new')

        models.JewelryCollection.objects.create(owner=user, kind=models.JewelryCollection.KIND_IDEABOOK, name='foo')
        response = self.get('/designer/upload/')
        self.assertNumCssMatches(1, response, '.collection-item')
        self.assertNumCssMatches(1, response, 'select#id_collection option')

        models.JewelryCollection.objects.create(owner=user, kind=models.JewelryCollection.KIND_DESIGNER, name='foo2')
        response = self.get('/designer/upload/')
        self.assertNumCssMatches(2, response, '.collection-item')
        self.assertNumCssMatches(2, response, 'select#id_collection option')

    def test_individual_item(self):
        user = create_and_login_user(self)
        authed = create_and_login_user(self)
        user.bio = '*fancy*'
        user.save()
        item = self.createItem(owner=user)

        unrelated = self.createItem(owner=user)
        collection = item.collections.first()
        other = self.createItem(owner=user, collection=collection)

        response = self.get(item.get_absolute_collection_url(collection))
        self.assertTrue('<p><em>fancy</em></p>' in response.content)
        self.assertEqual([other], response.context['related_collection'])
        self.assertEqual([], response.context['related_similar'])

    def test_collection_view(self):
        self.assertStatus(404, '/collection/1/')

        user = create_and_login_user(self)
        item = self.createItem(owner=user)
        collection = item.collections.first()
        collection.name = "My Collection?!"
        collection.save()

        url = collection.get_absolute_url()
        self.assertEquals(url, '/collection/1/my-collection/')

        self.get(url)

    def test_user_get_absolute_url(self):
        user = create_and_login_user(self)
        self.assertEquals(user.get_absolute_url(), '/profile/{}/charles-atterly/'.format(user.id))



