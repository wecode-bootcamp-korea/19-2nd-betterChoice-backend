import json
import bcrypt
import jwt
import my_settings

from django.test           import TestCase, Client

from users.models          import User

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

class SignInTest(TestCase):
    def setUp(self):
        User.objects.create(
            email     = 'test1@gmail.com',
            password  = bcrypt.hashpw('qwerqwerQWER!'.encode('utf-8'), bcrypt.gensalt()).decode('utf-8'),
            nickname  = 'test1',
            is_social = False
        )
    
    def tearDown(self):
        User.objects.all().delete()
    
    def test_success_signin(self):
        client = Client()
        user = {
            'email'    : 'test1@gmail.com',
            'password' : 'qwerqwerQWER!'
        }

        user_test    = User.objects.get(email='test1@gmail.com')
        access_token = jwt.encode({'id':user_test.id}, my_settings.SECRET['secret'], algorithm=my_settings.ALGORITHM)

        response = client.post('/users/signin', json.dumps(user), content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {'MESSAGE':'SUCCESS', 'ACCESS_TOKEN':access_token})
    
    def test_EMAIL_TYPE_ERROR_signin(self):
        client = Client()
        user = {
            'email'    : '',
            'password' : 'qwerqwerQWER!'
        }

        response = client.post('/users/signin', json.dumps(user), content_type='application/json')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {'MESSAGE':'EMAIL_TYPE_ERROR'})
    
    def test_PASSWORD_TYPE_ERROR_signin(self):
        client = Client()
        user = {
            'email'    : 'test!@gmail.com',
            'password' : ''
        }

        response = client.post('/users/signin', json.dumps(user), content_type='application/json')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {'MESSAGE':'PASSWORD_TYPE_ERROR'})

    def test_INVALID_EMAIL_signin(self):
        client = Client()
        user = {
            'email'    : 'test1@gmaill.com',
            'password' : 'qwerqwerQWER!'
        }

        response = client.post('/users/signin', json.dumps(user), content_type='application/json')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {'MESSAGE':'INVALID_EMAIL'})
    
    def test_INVALID_PASSWORD_signin(self):
        client = Client()
        user = {
            'email'    : 'test1@gmail.com',
            'password' : 'qwerqwerQWER!@'
        }

        response = client.post('/users/signin', json.dumps(user), content_type='application/json')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {'MESSAGE':'INVALID_PASSWORD'})
    
    def test_KEY_ERROR_signin(self):
        client = Client()
        user = {
            'password' : 'qwerqwerQWER!'
        }

        response = client.post('/users/signin', json.dumps(user), content_type='application/json')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {'MESSAGE':'KEY_ERROR'})
    
    def test_JSONDecodeError_signin(self):
        client = Client()
        user = {
            'email'    : 'test@gmail.com',
            'password' : 'qwerqwerQWER!'
        }

        response = client.post('/users/signin', user)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {'MESSAGE':'JSON_DECODE_ERROR'})