import bcrypt
import jwt
import json

from django.http  import JsonResponse

from my_settings import SECRET,ALGORITHM
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

