from django.urls import path
from users.views import kakaoView

from users.views import SignUpView, SignInView, SmsCheckView

urlpatterns = [
    path('/signup', SignUpView.as_view()),
    path('/signin', SignInView.as_view()),
    path('/sms-check', SmsCheckView.as_view()),
    path('/kakao-signin',kakaoView.as_view()),
]