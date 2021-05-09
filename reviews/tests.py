import my_settings
import bcrypt
import jwt
import json

from django.test         import TestCase, Client
from unittest.mock       import patch, MagicMock
from django.core.files   import File

from users.models        import User
from hotels.models       import Category, Location, Hotel, Room
from reservations.models import Reservation, Status
from reviews.models      import Review

class ReviewTest(TestCase):
    def setUp(self):
        
        Category.objects.create(
            id   = 1,
            name = '호텔'
        )

        Location.objects.create(
            id   = 1,
            name = '강남구'
        )

        User.objects.create(
            id           = 1,
            email        = 'qwer@gmail.com',
            password     = bcrypt.hashpw('qwerqwerQWER!'.encode('utf-8'), bcrypt.gensalt()).decode('utf-8'),
            nickname     = 'zzang',
            phone_number = '01012345678',
            is_social    = 'False'
        )

        self.token1 = jwt.encode({'id':1}, my_settings.SECRET['secret'], algorithm=my_settings.ALGORITHM)

        User.objects.create(
            id           = 2,
            email        = 'qwer2@gmail.com',
            password     = bcrypt.hashpw('qwerqwerQWER!'.encode('utf-8'), bcrypt.gensalt()).decode('utf-8'),
            nickname     = 'zzang2',
            phone_number = '01012345679',
            is_social    = 'False'
        )

        self.token2 = jwt.encode({'id':2}, my_settings.SECRET['secret'], algorithm=my_settings.ALGORITHM)

        Hotel.objects.create(
            id              = 1,
            name            = '최고호텔',
            address         = '강남구',
            thumbnail_image = 'qwerqwerqwer',
            longitude       = 12.21341231324,
            latitude        = 14.2345234524352345,
            category_id     = 1,
            location_id     = 1,
            star            = 5

        )

        Room.objects.create(
            id             = 1,
            name           = '스위트룸',
            image_url      = 'asdfasdfasdfasdf',
            original_price = 12000,
            discount_rate  = 0.05,
            occupancy      = 3,
            hotel_id       = 1,
        )

        Status.objects.create(
            id     = 2,
            status = '숙박완료'
        )
        
        Reservation.objects.create(
            id           = 1,
            name         = 'David',
            phone_number = '01012345678',
            check_in     = '2021-05-20',
            check_out    = '2021-05-22',
            status_id    = 2,
            user_id      = 1,
            hotel_id     = 1,
            room_id      = 1,
        )
        
        Review.objects.create(
            id             = 1,
            content        = '최고에요',
            rate           = 10.00,
            user_id        = 1,
            hotel_id       = 1,
            reservation_id = 1,
        )
    
    def tearDown(self):
        Review.objects.all().delete()
        Reservation.objects.all().delete()
        Status.objects.all().delete()
        Room.objects.all().delete()
        Hotel.objects.all().delete()
        User.objects.all().delete()
        Location.objects.all().delete()
        Category.objects.all().delete()
    
    def test_post_upload_no_file_success_ReviewView(self):
        client = Client()

        headers   = {'HTTP_Authorization' : self.token1}
        file_dict = {'content':'좋아요', 'rate':10.00}

        response  = client.post('/reviews/hotel/1', file_dict, **headers)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(),{'MESSAGE':'SUCCESS'})

    @patch("my_settings.S3_CLIENT")
    def test_post_upload_one_file_success_ReviewView(self, mocked_s3client):
        client  = Client()

        headers = {'HTTP_Authorization' : self.token1}

        mock_file                      = MagicMock(spec=File)
        mock_file.name                 = 'test1.jpg'
        mocked_s3client.upload_fileobj = MagicMock()

        file_dict = {'files':mock_file, 'content':'좋아요~', 'rate':10.00}

        response  = client.post('/reviews/hotel/1', file_dict, **headers)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(),{'MESSAGE':'SUCCESS'})
    
    @patch("my_settings.S3_CLIENT")
    def test_post_upload_multiple_files_success_ReviewView(self, mocked_s3client):
        client  = Client()

        headers = {'HTTP_Authorization' : self.token1}

        mock_file1                     = MagicMock(spec=File)
        mock_file2                     = MagicMock(spec=File)
        mock_file1.name                = 'test1.jpg'
        mock_file2.name                = 'test2.jpg'
        mocked_s3client.upload_fileobj = MagicMock()

        file_dict = {'files':[mock_file1,mock_file2], 'content':'좋아요~', 'rate':10.00}

        response  = client.post('/reviews/hotel/1', file_dict, **headers)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(),{'MESSAGE':'SUCCESS'})

    @patch("my_settings.S3_CLIENT")
    def test_post_HOTEL_DOES_NOT_EXIST_ReviewView(self, mocked_s3client):
        client  = Client()

        headers = {'HTTP_Authorization' : self.token1}

        mock_file1                     = MagicMock(spec=File)
        mock_file2                     = MagicMock(spec=File)
        mock_file1.name                = 'test1.jpg'
        mock_file2.name                = 'test2.jpg'
        mocked_s3client.upload_fileobj = MagicMock()

        file_dict = {'files':[mock_file1,mock_file2], 'content':'좋아요~', 'rate':10.00}

        response  = client.post('/reviews/hotel/2', file_dict, **headers)

        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json(),{'MESSAGE':'HOTEL_DOES_NOT_EXIST'})
    
    @patch("my_settings.S3_CLIENT")
    def test_post_UNAUTHORIZED_USER_ReviewView(self, mocked_s3client):
        client  = Client()

        headers = {'HTTP_Authorization' : self.token2}

        mock_file1                     = MagicMock(spec=File)
        mock_file2                     = MagicMock(spec=File)
        mock_file1.name                = 'test1.jpg'
        mock_file2.name                = 'test2.jpg'
        mocked_s3client.upload_fileobj = MagicMock()

        file_dict = {'files':[mock_file1,mock_file2], 'content':'좋아요~', 'rate':10.00}

        response  = client.post('/reviews/hotel/1', file_dict, **headers)

        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.json(),{'MESSAGE':'UNAUTHORIZED_USER'})
    
    @patch("my_settings.S3_CLIENT")
    def test_post_KEY_ERROR_ReviewView(self, mocked_s3client):
        client  = Client()

        headers = {'HTTP_Authorization' : self.token1}

        mock_file1                     = MagicMock(spec=File)
        mock_file2                     = MagicMock(spec=File)
        mock_file1.name                = 'test1.jpg'
        mock_file2.name                = 'test2.jpg'
        mocked_s3client.upload_fileobj = MagicMock()

        file_dict = {'files':[mock_file1,mock_file2], 'content':'좋아요~'}

        response  = client.post('/reviews/hotel/1', file_dict, **headers)

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(),{'MESSAGE':'KEY_ERROR'})
    
    def test_get_success_ReviewView(self):
        client   = Client()

        response = client.get('/reviews/hotel/1')
        review   = Review.objects.get(pk=1)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(),{'RESULTS':[{
            'content': '최고에요',
            'rate': '10.00',
            'rate_comment': '여기만한 곳은 어디에도 없을 거예요.',
            'nickname': 'zzang',
            'created_at': review.created_at.strftime('%Y-%m-%d %H:%M:%S'),
            'image_url': []}]})
    
    def test_get_HOTEL_DOES_NOT_EXIST_ReviewView(self):
        client   = Client()

        response = client.get('/reviews/hotel/2')

        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json(),{'MESSAGE':'HOTEL_DOES_NOT_EXIST'})
    
    def test_delete_success_ReviewView(self):
        client   = Client()

        headers  = {'HTTP_Authorization' : self.token1}
        response = client.delete('/reviews/1', **headers)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(),{'MESSAGE':'SUCCESS'})
    
    def test_delete_REVIEW_DOES_NOT_EXIST_ReviewView(self):
        client   = Client()

        headers  = {'HTTP_Authorization' : self.token1}
        response = client.delete('/reviews/2', **headers)

        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json(),{'MESSAGE':'REVIEW_DOES_NOT_EXIST'})

    def test_delete_UNAUTHORIZED_USER_ReviewView(self):
        client   = Client()

        headers  = {'HTTP_Authorization' : self.token2}
        response = client.delete('/reviews/1', **headers)

        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.json(),{'MESSAGE':'UNAUTHORIZED_USER'})