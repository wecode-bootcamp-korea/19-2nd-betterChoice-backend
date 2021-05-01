from django.urls import path

from users.views import SignUpView, SignInView

urlpatterns = [
    path('/signup', SignUpView.as_view()),
    path('/signin', SignInView.as_view())
]