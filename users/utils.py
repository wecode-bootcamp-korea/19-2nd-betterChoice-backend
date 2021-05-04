import bcrypt
import jwt
import json
import string
import random
import sys
import os
import hashlib
import hmac
import base64
import requests
import time

from django.http  import JsonResponse

from my_settings  import SECRET,ALGORITHM,ACCESS_KEY,SECRET_KEY,URI,URL,FROM_PHONE_NUMBER
from users.models import User

def LoginDecorator(func):
    def wrapper(self, request, *args, **kwargs):
        
        try:
            access_token       = request.headers['Authorization']
            check_access_token = jwt.decode(access_token, SECRET['secret'], algorithms=ALGORITHM)
            user               = User.objects.get(id=check_access_token['id'])
            request.user       = user

        except jwt.DecodeError:
            return JsonResponse({"error_code" : "INVALID_TOKEN"}, status=401)

        except User.DoesNotExist:
            return JsonResponse({"error_code" : "UNKNOWN_USER"}, status=401)

        return func(self, request, *args, **kwargs)
    return wrapper

def auth_number():
    length   = 4
    auth_num = ''

    for i in range(length):
        auth_num += random.choice(string.digits)
    
    return auth_num

def	make_signature():
    timestamp  = str(int(time.time() * 1000))
    access_key = ACCESS_KEY
    secret_key = SECRET_KEY
    method     = 'POST'
    uri        = URI

    message    = method + " " + uri + "\n" + timestamp + "\n" + access_key
    message    = bytes(message, 'UTF-8')
    signingKey = base64.b64encode(hmac.new(secret_key, message, digestmod=hashlib.sha256).digest())
    return signingKey

def send_sms(phone_number, auth_number):
    url        = URL
    timestamp  = str(int(time.time() * 1000))
    access_key = ACCESS_KEY
    SIGNATURE  = make_signature()

    body = {
        "type"        : "SMS",
        "contentType" : "COMM",
        "from"        : FROM_PHONE_NUMBER,
        "content"     : f"[야,여기어때] 인증 번호 [{auth_number}]를 입력해주세요.",
        "messages"    : [{"to":phone_number}]
    }

    headers = {
        "Content-Type"             : "application/json; charset=utf-8",
        "x-ncp-apigw-timestamp"    : timestamp,
        "x-ncp-iam-access-key"     : access_key,
        "x-ncp-apigw-signature-v2" : SIGNATURE
    }

    requests.post(url, data=json.dumps(body), headers=headers)