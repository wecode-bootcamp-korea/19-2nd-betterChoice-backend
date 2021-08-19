import json
import boto3
import my_settings

from django.views import View
from django.http  import JsonResponse

from reviews.models      import Review, ReviewImage
from hotels.models       import Hotel
from reservations.models import Reservation
from users.utils         import LoginDecorator

class ReviewView(View):
    @LoginDecorator
    def post(self, request, hotel_id):
        try:
            content     = request.POST['content']
            rate        = request.POST['rate']
            files       = request.FILES.getlist('files', None)
            s3_client   = my_settings.S3_CLIENT
            user        = request.user
            reservation = Reservation.objects.filter(user=user, hotel=hotel_id, status=2)
            hotel_exist = Hotel.objects.filter(id=hotel_id).exists()

            if not hotel_id or not hotel_exist:
                return JsonResponse({'MESSAGE':'HOTEL_DOES_NOT_EXIST'}, status=404)
            
            if not reservation.exists():
                return JsonResponse({'MESSAGE':'UNAUTHORIZED_USER'}, status=401)

            review = Review.objects.create(
                content     = content,
                rate        = rate,
                hotel_id    = hotel_id,
                user        = user,
                reservation = reservation.order_by('-created_at').first(),
            )

            for file in files:
                s3_client.upload_fileobj(
                    file,
                    my_settings.AWS_S3_BUCKET_NAME,
                    file.name,
                    ExtraArgs = {
                        "ContentType" : file.content_type
                    }
                )
            
            review.reviewimage_set.bulk_create([
                ReviewImage(
                image_url = f'https://{my_settings.AWS_S3_BUCKET_NAME}.s3.ap-northeast-2.amazonaws.com/{file.name}',
                review    = review
                ) for file in files ])
            
            return JsonResponse({'MESSAGE':'SUCCESS'}, status=200)
            
        except KeyError:
            return JsonResponse({'MESSAGE': 'KEY_ERROR'}, status=400)

        except json.JSONDecodeError:
            return JsonResponse({'MESSAGE': 'JSON_DECODE_ERROR'}, status=400)
    
    def get(self, request, hotel_id):
        hotel_exist = Hotel.objects.filter(id=hotel_id).exists()

        if not hotel_id or not hotel_exist:
            return JsonResponse({'MESSAGE':'HOTEL_DOES_NOT_EXIST'}, status=404)

        reviews = Review.objects.filter(hotel=hotel_id)

        results = [{
            'content'      : review.content,
            'rate'         : review.rate,
            'rate_comment' : '여기만한 곳은 어디에도 없을 거예요.' if review.rate == 10.00 else '만족해요',
            'nickname'     : review.user.nickname,
            'created_at'   : review.created_at.strftime('%Y-%m-%d %H:%M:%S'),
            'image_url'    : [review_image.image_url for review_image in review.reviewimage_set.all()]
        } for review in reviews ]

        return JsonResponse({'RESULTS':results}, status=200)
    
    @LoginDecorator
    def delete(self, request, review_id):
        review_exist = Review.objects.filter(id=review_id).exists()

        if not review_id or not review_exist:
            return JsonResponse({'MESSAGE':'REVIEW_DOES_NOT_EXIST'}, status=404)

        user   = request.user
        review = Review.objects.filter(user=user, id=review_id).exists()

        if not review:
            return JsonResponse({'MESSAGE':'UNAUTHORIZED_USER'}, status=401)
            
        Review.objects.get(user=user, id=review_id).delete()
        
        return JsonResponse({'MESSAGE':'SUCCESS'}, status=200)