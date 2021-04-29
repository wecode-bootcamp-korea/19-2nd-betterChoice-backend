import json
import bcrypt
import jwt
import my_settings

from django.test           import TestCase, Client
from unittest.mock         import patch, MagicMock

from users.models          import User, PhoneCheck

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
        self.assertEqual(response.json(), {'MESSAGE':'SUCCESS', 'ACCESS_TOKEN':access_token, 'NICKNAME':user_test.nickname})
    
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

class SmsCheckTest(TestCase):
    def setUp(self):
        PhoneCheck.objects.create(
            phone_number = '01012345678',
            auth_number  = 1234
        )
    
    def tearDown(self):
        PhoneCheck.objects.all().delete()
    
    @patch("users.utils.requests")
    def test_post_success_SmsCheck(self, mocked_requests):
        client = Client()

        class MockedResponse:
            def json(self):
                return {
                    "content" : "[야,여기어때] 인증 번호 [1234]를 입력해주세요."
                }
        
        mocked_requests.post = MagicMock(return_value = MockedResponse())

        user = {
            'phone_number' : '01012345678'
        }

        response = client.post('/users/sms-check', json.dumps(user), content_type='application/json')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {'MESSAGE':'SUCCESS'})
    
    def test_post_INVALID_PHONE_NUMBER_SmsCheck(self):
        client = Client()

        user = {
            'phone_number' : '010-1234-5678'
        }

        response = client.post('/users/sms-check', json.dumps(user), content_type='application/json')

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {'MESSAGE':'INVALID_PHONE_NUMBER'})
    
    def test_post_KEY_ERROR_SmsCheck(self):
        client = Client()

        user = {

        }

        response = client.post('/users/sms-check', json.dumps(user), content_type='application/json')

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {'MESSAGE':'KEY_ERROR'})
    
    def test_post_JSONDecodeError_SmsCheck(self):
        client = Client()

        user = {
            'phone_number' : '01012345678'
        }

        response = client.post('/users/sms-check', user)

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {'MESSAGE':'JSON_DECODE_ERROR'})
    
    def test_get_success_SmsCheck(self):
        client = Client()

        response = client.get('/users/sms-check?phone_number=01012345678&auth_number=1234')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {'MESSAGE':'SUCCESS'})

    def test_get_INVALID_AUTH_NUMBER_SmsCheck(self):
        client = Client()

        response = client.get('/users/sms-check?phone_number=01012345678&auth_number=4321')

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {'MESSAGE':'INVALID_AUTH_NUMBER'})

class KakaoTestCase(TestCase):
    @patch("users.views.requests")
    def test_user_kakao_post_success(self, mocked_requests):

        class MockedResponse:
            def json(self):
                return {
                  "id": 123456,
                  "kakao_account": {
                    "profile": {
                      "nickname": "test"
                    },
                    "email": "test1@kakao.com"
                  }
                }
        mocked_requests.get = MagicMock(return_value=MockedResponse())

        client = Client()
        header = {'HTTP_Authorization': "access_token"}
        response = client.post("/users/kakao-signin", **header, content_type="application/json")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.json(),
            {
                "TOKEN": response.json()['TOKEN'], "NICKNAME": "test"
            }
        )

    def test_user_kakao_post_keyerror(self):
        client = Client()
        headers = {'HTTP_Authorization': "access_token"}
        response = client.post("/users/kakao-signin", **headers, content_type="application/json")
        self.assertEqual(response.status_code,401)