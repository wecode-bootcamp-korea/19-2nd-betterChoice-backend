import json

from django.test  import TestCase, Client

from users.models import User

class SingUpTest(TestCase):
    def setUp(self):
        User.objects.create(
            email     = 'test1@gmail.com',
            password  = 'qwerqwerQWER!',
            nickname  = 'test1',
            is_social = False
        )
    
    def tearDown(self):
        User.objects.all().delete()

    def test_success_signup(self):
        client = Client()
        user = {
            'email'     : 'test2@gmail.com',
            'password'  : 'qwerqwerQWER!',
            'nickname'  : 'test2',
            'is_social' : False
        }
        response = client.post('/users/signup', json.dumps(user), content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {'MESSAGE':'SUCCESS'})
    
    def test_fail_signup_email_form(self):
        client = Client()
        user = {
            'email'     : 'test2gmailcom',
            'password'  : 'qwerqwerQWER!',
            'nickname'  : 'test3',
            'is_social' : False
        }
        response = client.post('/users/signup', json.dumps(user), content_type='application/json')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {'MESSAGE':'INVALID_EMAIL'})
    
    def test_fail_signup_password_form(self):
        client = Client()
        user = {
            'email'     : 'test3@gmail.com',
            'password'  : 'qwerqwer',
            'nickname'  : 'test3',
            'is_social' : False
        }
        response = client.post('/users/signup', json.dumps(user), content_type='application/json')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {'MESSAGE':'INVALID_PASSWORD'})

    def test_fail_signup_email_duplicate(self):
        client = Client()
        user = {
            'email'     : 'test1@gmail.com',
            'password'  : 'qwerqwerQWER!',
            'nickname'  : 'test3',
            'is_social' : False
        }
        response = client.post('/users/signup', json.dumps(user), content_type='application/json')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {'MESSAGE':'EMAIL_ALREADY_EXIST'})
    
    def test_fail_signup_nickname_duplicate(self):
        client = Client()
        user = {
            'email'     : 'test3@gmail.com',
            'password'  : 'qwerqwerQWER!',
            'nickname'  : 'test1',
            'is_social' : False
        }
        response = client.post('/users/signup', json.dumps(user), content_type='application/json')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {'MESSAGE':'NICKNAME_ALREADY_EXIST'})
    
    def test_KeyError_signup(self):
        client = Client()
        user = {
            'password'  : 'qwerqwerQWER!',
            'nickname'  : 'test3',
            'is_social' : False
        }
        response = client.post('/users/signup', json.dumps(user), content_type='application/json')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {'MESSAGE':'KEY_ERROR'})

    def test_JSONDecodeError_signup(self):
        client = Client()
        user = {
            'email'     : 'test3@gmail.com',
            'password'  : 'qwerqwerQWER!',
            'nickname'  : 'test3',
            'is_social' : False
        }

        response = client.post('/users/signup', user)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {'MESSAGE':'JSON_DECODE_ERROR'})
