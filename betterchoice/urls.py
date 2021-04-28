from django.urls import path, include

urlpatterns = [
    path('users', include('users.urls')),
    path('hotels', include('hotels.urls')),
    path('reservations', include('reservations.urls')),
    path('reviews', include('reviews.urls')),
]
