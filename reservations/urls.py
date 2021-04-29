from django.urls import path
from reservations.views import ReservationView

urlpatterns = [
    path('', ReservationView.as_view()),
]