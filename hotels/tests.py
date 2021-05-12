import json

from django.test import TestCase, Client, client

from users.models       import User
from reservations.models import Reservation, Status
from reviews.models      import Review
from hotels.models      import (
    Category, HotelImage, Location, CategoryLocation, Hotel, Room, ReservationCheck
)

client = Client()

class CategoryLocationTest(TestCase):
    def setUp(self):
        Category.objects.create(
                name            = '호텔',
                thumbnail_image = 'test_url',
                id              = 1
                )
        
        Location.objects.create(
                name = '강남',
                id   = 1
                )

        CategoryLocation.objects.create(
                category = Category.objects.get(id=1),
                location = Location.objects.get(id=1)
                )

    def tearDown(self):
        Category.objects.all().delete(),
        Location.objects.all().delete(),
        CategoryLocation.objects.all().delete()

    def test_get_categorylocation_success(self):
        response = client.get('/hotels/main')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(),{'MESSAGE':'SUCCESS',
            'results' : [
                {
                    'category'  : '호텔',
                    'image_url' : 'test_url',
                    'location'  : '강남',
                    }
                ]
            }
        )

class HotelTest(TestCase):
    def setUp(self):
        Category.objects.create(
            name            = '호텔',
            thumbnail_image = 'test_url',
            id              = 1
            )

        Location.objects.create(
            name = '강남',
            id   = 1
            )

        CategoryLocation.objects.create(
                category = Category.objects.get(id=1),
                location = Location.objects.get(id=1)
                )

        Hotel.objects.create(
                name            = '호텔이름',
                address         = '주소',
                thumbnail_image = 'test_url',
                longitude       = '111.11111111111111111111',
                latitude        = '222.22222222222222222222',
                star            = 5,
                id              = 1,
                category        = Category.objects.get(id=1),
                location        = Location.objects.get(id=1)
                )

        Room.objects.create(
                name           = '방이름',
                image_url      = 'test_url',
                original_price = 10000,
                discount_rate  = 0.8,
                occupancy      = 2,
                hotel          = Hotel.objects.get(id=1),
                id             = 1
                )

        ReservationCheck.objects.create(
                date     = '2021-05-07',
                quantity = 10,
                remain   = 5,
                room     = Room.objects.get(id=1),
                id       = 1
                )

        User.objects.create(
                email     = '1111@naver.com',
                password  = 'qwerqwerQWER!',
                nickname  = '1111',
                is_social = False,
                id        = 1
                )

        Status.objects.create(
                status = '예약완료',
                id     = 1
                )

        Reservation.objects.create(
                name         = 'test',
                phone_number = '01011111111',
                check_in     = '2021-05-07',
                check_out    = '2021-05-08',
                status       = Status.objects.get(id=1),
                hotel        = Hotel.objects.get(id=1),
                room         = Room.objects.get(id=1),
                user         = User.objects.get(id=1),
                id           = 1
                )

        Review.objects.create(
                content        = 'good',
                rate           = 10,
                user           = User.objects.get(id=1),
                hotel          = Hotel.objects.get(id=1),
                reservation    = Reservation.objects.get(id=1),
                id             = 1
                )

    def tearDown(self):
        Category.objects.all().delete(),
        Location.objects.all().delete(),
        Hotel.objects.all().delete(),
        Room.objects.all().delete,
        ReservationCheck.objects.all().delete(),
        User.objects.all().delete(),
        Status.objects.all().delete(),
        Reservation.objects.all().delete(),
        Review.objects.all().delete()

    def test_get_hotel_success(self):
        response = client.get('/hotels?star=5&sort_type=1')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(),{'MESSAGE':'SUCCESS',
            'results' : [
                {
                    'id'                   : 1,
                    'name'                 : '호텔이름',
                    'address'              : '주소',
                    'thumbnail_image'      : 'test_url',
                    'star'                 : 5,
                    'lowest_original_price': 10000,
                    'lowest_discount_price': 8000,
                    'hotel_review_rate'    : 10,
                    'remain'               : 5
                    }
                ]
            }
        )

    def test_get_hotel_invalid_occupancy(self):
        response = client.get('/hotels?star=5&sort_type=1&occupancy=5')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(),{'MESSAGE':'INVALID_OCCUPANCY'})
    
    def test_get_hotel_invalid_star(self):
        response = client.get('/hotels?star=6&sort_type=1')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(),{'MESSAGE':'INVALID_STAR'})

    def test_get_hotel_invalid_date(self):
        response = client.get('/hotels?star=5&sort_type=1&check_in=2021-05-07&check_out=2021-05-06')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(),{'MESSAGE':'INVALID_DATE'})
    
    def test_get_hotel_key_error(self):
        response = client.get('/hotels')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {'MESSAGE':'KEY_ERROR'})
    
    def test_get_hotel_value_error(self):
        response = client.get('/hotels?star="hello"&sort_type=1')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {'MESSAGE':'VALUE_ERROR'})

class HotelDetailTest(TestCase):
    def setUp(self):
        Category.objects.create(
            name            = '호텔',
            thumbnail_image = 'test_url',
            id              = 1
            )

        Location.objects.create(
            name = '강남',
            id   = 1
            )

        CategoryLocation.objects.create(
                category = Category.objects.get(id=1),
                location = Location.objects.get(id=1)
                )
        
        Hotel.objects.create(
                name            = '호텔이름',
                address         = '주소',
                thumbnail_image = 'test_url',
                longitude       = '111.11111111111111111111',
                latitude        = '222.22222222222222222222',
                star            = 5,
                id              = 1,
                category        = Category.objects.get(id=1),
                location        = Location.objects.get(id=1)
                )

        HotelImage.objects.create(
                image_url = 'test_url',
                hotel     = Hotel.objects.get(id=1)
                )

        Room.objects.create(
                name           = '방이름',
                image_url      = 'test_url',
                original_price = 10000,
                discount_rate  = 0.8,
                occupancy      = 2,
                hotel          = Hotel.objects.get(id=1),
                id             = 1
                )

        ReservationCheck.objects.create(
                date     = '2021-05-07',
                quantity = 10,
                remain   = 5,
                room     = Room.objects.get(id=1),
                id       = 1
                )

        User.objects.create(
                email     = '1111@naver.com',
                password  = 'qwerqwerQWER!',
                nickname  = '1111',
                is_social = False,
                id        = 1
                )

        Status.objects.create(
                status = '예약완료',
                id     = 1
                )

        Reservation.objects.create(
                name         = 'test',
                phone_number = '01011111111',
                check_in     = '2021-05-07',
                check_out    = '2021-05-08',
                status       = Status.objects.get(id=1),
                hotel        = Hotel.objects.get(id=1),
                room         = Room.objects.get(id=1),
                user         = User.objects.get(id=1),
                id           = 1
                )

        Review.objects.create(
                content        = 'good',
                rate           = 10,
                user           = User.objects.get(id=1),
                hotel          = Hotel.objects.get(id=1),
                reservation    = Reservation.objects.get(id=1),
                id             = 1
                )

    def tearDown(self):
        Category.objects.all().delete(),
        Location.objects.all().delete(),
        CategoryLocation.objects.all().delete(),
        Hotel.objects.all().delete(),
        HotelImage.objects.all().delete(),
        Room.objects.all().delete,
        ReservationCheck.objects.all().delete(),
        User.objects.all().delete(),
        Status.objects.all().delete(),
        Reservation.objects.all().delete(),
        Review.objects.all().delete()

    def test_get_hoteldetail_success(self):
        response = client.get('/hotels/1?check_in=2021-05-07&check_out=2021-05-08')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {'MESSAGE':'SUCCESS',
            'results': {
                'id'                    : 1,
                'hotel_name'            : '호텔이름',
                'star'                  : 5,
                'address'               : '주소',
                'longitude'             : '111.11111111111111111111',
                'latitude'              : '222.22222222222222222222',
                'hotel_thumbnail_image' : 'test_url',
                'hotel_image'           : ['test_url'],
                'hotel_review_rate'     : 10,
                'room_type'             : [
                    {
                        'image'         : 'test_url',
                        'room_name'     : '방이름',
                        'original_price': 10000,
                        'discount_price': 8000,
                        'remain'        : 5
                        }
                    ]
                }
            }
        )

    def test_get_hoteldetail_invalid_hotel(self):
        response = client.get('/hotels/2?check_in=2021-05-07&check_out=2021-05-08')
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json(), {'MESSAGE':'INVALID_HOTEL'})
    
    def test_get_hoteldetail_value_error(self):
        response = client.get('/hotels/1?check_in=2021-05-07&check_outttt=2021-05-08')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {'MESSAGE':'VALUE_ERROR'})

    def test_get_hoteldetail_validation_error(self):
        response = client.get('/hotels/1?check_in=2021-05-07&check_out=2021-05-0')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {'MESSAGE':'VALIDATION_ERROR'})
