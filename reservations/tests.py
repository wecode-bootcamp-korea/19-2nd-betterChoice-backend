import json
import bcrypt
import jwt
import my_settings

from django.test           import TestCase, Client

from reservations.models import *
from users.models import *
from hotels.models import *
from django.db import transaction

class ReservationTestCase(TestCase):

    def setUp(self):
        Status.objects.create(
            status="예약완료",
            id=1,
        )
        Location.objects.create(
            name='강남',
            id=1,
        )
        Category.objects.create(
            name='호텔',
            thumbnail_image='image_url',
            id=1,
        )
        Hotel.objects.create(
            name = "test hotel",
            address= "강남구 어쩌고 21",
            thumbnail_image='image_url',
            longitude='122.12112',
            latitude='3232.32323',
            category=Category.objects.get(id=1),
            location=Location.objects.get(id=1),
            star=5,
            id=1,
        )
        Room.objects.create(
            name="디럭스룸",
            image_url='image_url',
            original_price='150000.00',
            discount_rate='0.9',
            occupancy=2,
            hotel=Hotel.objects.get(id=1),
            id=1,
        )
        Coupon.objects.create(
            name="1만원 할인 쿠폰",
            id=1,

        )
        User.objects.create(
            email = "test1@gmail.com",
            password='123456789',
            phone_number='01012341234',
            nickname="tset1",
            is_social=1,
            id=1,
        )
        UserCoupon.objects.create(
            coupon=Coupon.objects.get(id=1),
            user=User.objects.get(id=1),
            is_coupon=False,
            id=1,
        )
        self.token = jwt.encode({'id':User.objects.get(email='test1@gmail.com').id},my_settings.SECRET['secret'],algorithm =my_settings.ALGORITHM)

        ReservationCheck.objects.create(
            date='2021-05-07',
            quantity=10,
            remain=10,
            room=Room.objects.get(id=1),
            id=1,

        )

    def tearDown(self):
        Reservation.objects.all().delete()

    def test_reservationview_post_success(self):
        client = Client()
        headers = {'HTTP_Authorization': self.token}

        reservation = {
            "name" : "test2",
            "phone_number" : "01023452345",
            "check_in" : "2021-05-07",
            "check_out" : "2021-05-08",
            "hotel" : 1,
            "room": 1,
            "user": 1,
            "status": 1,
        }

        response = client.post('/reservations', json.dumps(reservation), **headers, content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(),
                         {
                             'MESSAGE':'SUCCESS'
                         }
                    )

    def test_reservationview_post_no_information(self):
        client = Client()
        headers = {'HTTP_Authorization': self.token}

        Reservation = {
            "name" : "",
            "phone_number": "33",
            "check_in": "2021-05-07",
            "check_out": "2021-05-08",
            "hotel": 1,
            "room": 1,
            "user": 1,
        }

        response = client.post('/reservations', json.dumps(Reservation), **headers, content_type='application/json')
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json(),
                         {
                             'MESSAGE':'NO_INFORMATION'
                         }
                    )

    def test_reservationview_post_keyerror(self):
        client = Client()
        headers = {'HTTP_Authorization': self.token}

        Reservation = {
            "phone_number": "01023452345",
            "check_in": "2021-05-07",
            "check_out": "2021-05-08",
            "hotel": 1,
            "room": 1,
            "user": 1,
        }

        response = client.post('/reservations', json.dumps(Reservation), **headers, content_type='application/json')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(),
                         {
                             'MESSAGE':'KEY_ERROR'
                         }
                    )

    def test_reservationview_post_no_hotel(self):
        client = Client()
        headers = {'HTTP_Authorization': self.token}

        Reservation = {
            "name": "test2",
            "phone_number": "01023452345",
            "check_in": "2021-05-07",
            "check_out": "2021-05-08",
            "hotel": 3,
            "room": 1,
            "user": 1,
            "status": 1,
        }

        response = client.post('/reservations', json.dumps(Reservation), **headers, content_type='application/json')
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json(),
                         {
                             'MESSAGE':'NO_HOTEL'
                         }
                         )

    def test_reservationview_post_no_room(self):
        client = Client()
        headers = {'HTTP_Authorization': self.token}

        Reservation = {
            "name": "test2",
            "phone_number": "01023452345",
            "check_in": "2021-05-07",
            "check_out": "2021-05-08",
            "hotel": 1,
            "room": 3,
            "user": 1,
            "status": 1,
        }

        response = client.post('/reservations', json.dumps(Reservation), **headers, content_type='application/json')
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json(),
                         {
                             'MESSAGE':'NO_ROOM'
                         }
                         )

    def test_reservationview_post_validation(self):
        client = Client()
        headers = {'HTTP_Authorization': self.token}
        reservation = {
            "name": "test2",
            "phone_number": "01023452345",
            "check_in": "",
            "check_out": "2021-05-08",
            "hotel": 1,
            "room": 1,
            "user": 1,
            "status": 1,
        }

        response = client.post('/reservations', json.dumps(reservation), **headers, content_type='application/json')
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json(),
                         {
                             'MESSAGE': 'VALIDATION_ERROR'
                         }
                         )

    def test_reservationview_post_no_remain_room(self):
        client  = Client()
        headers = {'HTTP_Authorization': self.token}

        remain = ReservationCheck.objects.filter(id=1).update(remain=0)

        reservation = {
            "name": "test2",
            "phone_number": "01023452345",
            "check_in": "2021-05-07",
            "check_out": "2021-05-08",
            "hotel": 1,
            "room": 1,
            "user": 1,
            "status": 1,
        }
        response = client.post('/reservations', json.dumps(reservation), **headers, content_type='application/json')

        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json(),
                         {
                             "MESSAGE": "NO_REMAIN_ROOM"
                         }
                         )

    def test_reservationview_get_success(self):
        client = Client()
        headers = {'HTTP_Authorization': self.token}

        reservation = {
            "name": "test2",
            "phone_number": "01023452345",
            "check_in": "2021-05-07",
            "check_out": "2021-05-08",
            "hotel": 1,
            "room": 1,
            "user": 1,
            "status": 1,
        }

        response = client.post('/reservations', json.dumps(reservation), **headers, content_type='application/json')
        response = client.get('/reservations', **headers, content_type='application/json')
        self.assertEqual(response.json(),
                 {
                     "RESULTS": [
                         {
                             "name": "test2",
                             "phone_number": "01023452345",
                             "check_in": "2021-05-07",
                             "check_out": "2021-05-08",
                             "status": "예약완료",
                             "hotel": "test hotel",
                             "image_url": "image_url",
                             "price": 135000
                         }
                    ]
                 }
            )
        self.assertEqual(response.status_code, 200)