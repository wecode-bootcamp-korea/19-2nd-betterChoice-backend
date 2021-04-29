from django.urls import path

from hotels.views import CategoryLocationView, HotelDetailView, HotelView

urlpatterns = [
        path('/main', CategoryLocationView.as_view()),
        path('', HotelView.as_view()),
        path('/<int:hotel_id>', HotelDetailView.as_view())
]
