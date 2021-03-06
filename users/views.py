import bcrypt
import jwt
import json
import my_settings
import requests

from django.views          import View
from django.http           import JsonResponse

from users.models          import User, UserCoupon, Coupon, UserLike, PhoneCheck
from users.utils           import auth_number, make_signature, send_sms

class SignUpView(View):
    def post(self, request):

        try:
            data     = json.loads(request.body)
            email    = data['email']
            password = data['password']
            nickname = data['nickname']

            if not my_settings.EMAIL_CHECK.match(email):
                return JsonResponse({'MESSAGE':'INVALID_EMAIL'}, status=400)
            
            if not my_settings.PASSWORD_CHECK.match(password):
                return JsonResponse({'MESSAGE':'INVALID_PASSWORD'}, status=400)
            
            if User.objects.filter(email=email).exists():
                return JsonResponse({'MESSAGE':'EMAIL_ALREADY_EXIST'}, status=400)
            
            if User.objects.filter(nickname=nickname).exists():
                return JsonResponse({'MESSAGE':'NICKNAME_ALREADY_EXIST'}, status=400)
            
            hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
            hashed_password = hashed_password.decode('utf-8')
            
            User.objects.create(
                email     = email,
                password  = hashed_password,
                nickname  = nickname,
                is_social = False
            )

            return JsonResponse({'MESSAGE':'SUCCESS'}, status=200)

        except KeyError:
            return JsonResponse({'MESSAGE':'KEY_ERROR'}, status=400)
        
        except json.JSONDecodeError:
            return JsonResponse({'MESSAGE': 'JSON_DECODE_ERROR'}, status=400)

class SignInView(View):
    def post(self, request):

        try:
            data     = json.loads(request.body)
            email    = data['email']
            password = data['password']

            if not email:
                return JsonResponse({'MESSAGE':'EMAIL_TYPE_ERROR'}, status=400)
            
            if not password:
                return JsonResponse({'MESSAGE':'PASSWORD_TYPE_ERROR'}, status=400)

            if not User.objects.filter(email=email).exists():
                return JsonResponse({'MESSAGE':'INVALID_EMAIL'}, status=400)
            
            user             = User.objects.get(email=email)
            encode_password  = user.password.encode('utf-8')
            checked_password = bcrypt.checkpw(password.encode('utf-8'), encode_password)

            if not checked_password:
                return JsonResponse({'MESSAGE':'INVALID_PASSWORD'}, status=400)
            
            access_token = jwt.encode({'id':user.id}, my_settings.SECRET['secret'], algorithm=my_settings.ALGORITHM)
            return JsonResponse({'MESSAGE':'SUCCESS', 'ACCESS_TOKEN':access_token, 'NICKNAME':user.nickname}, status=200)

        except KeyError:
            return JsonResponse({'MESSAGE':'KEY_ERROR'}, status=400)
        
        except json.JSONDecodeError:
            return JsonResponse({'MESSAGE': 'JSON_DECODE_ERROR'}, status=400)

class SmsCheckView(View):
    def post(self, request):
        auth_num = auth_number()
        
        try:
            data         = json.loads(request.body)
            phone_number = data['phone_number']

            if not my_settings.PHONE_CHECK.match(phone_number):
                return JsonResponse({'MESSAGE':'INVALID_PHONE_NUMBER'}, status=400)

            PhoneCheck.objects.update_or_create(phone_number=phone_number,defaults={'auth_number':auth_num})

            send_sms(phone_number = phone_number, auth_number = auth_num)

            return JsonResponse({'MESSAGE': 'SUCCESS'}, status=200)

        except KeyError:
            return JsonResponse({'MESSAGE': 'KEY_ERROR'}, status=400)
            
        except json.JSONDecodeError:
            return JsonResponse({'MESSAGE': 'JSON_DECODE_ERROR'}, status=400)

    def get(self, request):
        auth_number  = request.GET.get('auth_number', None)
        phone_number = request.GET.get('phone_number', None)
        phone_check  = PhoneCheck.objects.filter(phone_number=phone_number, auth_number=auth_number).exists()

        if not phone_check:
            return JsonResponse({'MESSAGE':'INVALID_AUTH_NUMBER'}, status=400)
        
        return JsonResponse({'MESSAGE':'SUCCESS'}, status=200)

class kakaoView(View):
    def post(self, request):
        try:
            access_token = request.headers.get('Authorization', None)
            url          = 'https://kapi.kakao.com/v2/user/me'
            headers      = {'Authorization': f'Bearer {access_token}',
                            'Content-type': 'application/x-www-form-urlencoded;charset=utf-8'
            }

            response      = requests.get(url,headers=headers)
            data          = response.json()
            kakao_user_id = data['id']
            email         = data['kakao_account']['email']
            nickname      = data['kakao_account']['profile']['nickname']

            if not User.objects.filter(kakao_user_id=kakao_user_id).exists():
                User.objects.create(
                    kakao_user_id = kakao_user_id,
                    email         = email,
                    nickname      = nickname,
                    is_social     = True
                )

            token = jwt.encode({'id': User.objects.get(kakao_user_id=kakao_user_id).id}, my_settings.SECRET['secret'], algorithm=my_settings.ALGORITHM)
            return JsonResponse({'TOKEN': token, 'NICKNAME': nickname},status=200)

        except KeyError:
            return JsonResponse({'MESSAGE': 'KEY_ERROR'},status=401)