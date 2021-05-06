import json

from django.http            import JsonResponse
from django.views           import View
from json.decoder           import JSONDecodeError
from django.core.exceptions import ObjectDoesNotExist
from django.db.models       import Q, Avg, Min

from hotels.models import Category, Hotel

class CategoryLocationView(View):
    def get(self, request):
        results = [
                {
                    'location'  : category.location.get(id=category.id).name,
                    'category'  : category.name,
                    'image_url' : category.thumbnail_image
                    }for category in Category.objects.all().prefetch_related('location')]

        return JsonResponse({'MESSAGE':'SUCCESS', 'results':results}, status=200)

class HotelView(View):
    def get(self, request):
        try:
            category_name = request.GET.get('category_name')
            location_name = request.GET.get('location_name')
            occupancy     = request.GET.get('occupancy')
            star          = request.GET.get('star')
            check_in      = request.GET.get('check_in')
            check_out     = request.GET.get('check_out')
            sort_type     = request.GET.get('sort_type')
            search        = request.GET.get('search')

            hotel_filter = Q()
            
            if category_name:
                hotel_filter.add((
                    Q(category__name = category_name)
                    ), Q.AND)

            if location_name:
                hotel_filter.add((
                    Q(location__name = location_name)
                    ), Q.AND)

            if occupancy:
                hotel_filter.add((
                    Q(room__occupancy__gte = occupancy)
                    ), Q.AND)
                if int(occupancy) >= 5:
                    return JsonResponse({'MESSAGE':'INVALID_OCCUPANCY'}, status=400)

            if star:
                hotel_filter.add((
                    Q(star = star)
                    ), Q.AND)
                if (int(star) > 5 or int(star) < 1):
                    return JsonResponse({'MESSAGE':'INVALID_STAR'}, status=400)

            if check_in and check_out:
                hotel_filter.add((
                    Q(room__reservationcheck__date__gte = check_in) &
                    Q(room__reservationcheck__date__lt  = check_out)
                    ), Q.AND)
                if check_in >= check_out:
                    return JsonResponse({'MESSAGE':'INVALID_DATE'}, status=400)
            hotel_lists = Hotel.objects.filter(hotel_filter).distinct()
            
            sort_lists = {
                    '1' : '?',
                    '2' : '-rate',
                    '3' : 'price',
                    '4' : '-price',
                    }

            if sort_type == '2':
                    hotel_lists = hotel_lists.annotate(rate = Avg('review__rate')).order_by(sort_lists[sort_type])
            
            hotel_lists = hotel_lists.annotate(price = Min('room__original_price')).order_by(sort_lists[sort_type])

            if search:
                hotel_lists = Hotel.objects.filter(name__icontains = search)
            
            results = [
                    {
                        'id'                    : hotel.id,
                        'name'                  : hotel.name,
                        'address'               : hotel.address,
                        'thumbnail_image'       : hotel.thumbnail_image,
                        'star'                  : hotel.star,
                        'lowest_original_price' : int(hotel.room_set.all().order_by('original_price').first().original_price),
                        'lowest_discount_price' : int(hotel.room_set.order_by('original_price').first().original_price * hotel.room_set.order_by('original_price').first().discount_rate),
                        'hotel_review_rate' : float(hotel.review_set.aggregate(Avg('rate'))['rate__avg']) if hotel.review_set.all() else None,
                        'remain'            : min([int(room.reservationcheck_set.all().order_by('remain').first().remain) for room in hotel.room_set.all()])
                        }for hotel in hotel_lists]
            
            return JsonResponse({'MESSAGE':'SUCCESS', 'results':results}, status = 200)
        except KeyError:
            return JsonResponse({'MESSAGE':'KEY_ERROR'}, status=400)
        except ValueError:
            return JsonResponse({'MESSAGE':'VALUE_ERROR'}, status=400)

class HotelDetailView(View):
    def get(self, request, hotel_id):
        try:
            check_in      = request.GET.get('check_in')
            check_out     = request.GET.get('check_out')
            
            if not Hotel.objects.filter(id = hotel_id).exists():
                return JsonResponse({'MESSAGE':'INVALID_HOTEL'}, status=404)

            hotel = Hotel.objects.filter(
                    Q(id = hotel_id) &
                    (
                        Q(room__reservationcheck__date__gte = check_in) & 
                        Q(room__reservationcheck__date__lt  = check_out)
                        )
                    ).first()

            results = {
                'hotel_name'            : hotel.name,
                'star'                  : hotel.star,
                'address'               : hotel.address,
                'longitude'             : hotel.longitude,
                'latitude'              : hotel.latitude,
                'hotel_thumbnail_image' : hotel.thumbnail_image,
                'hotel_image'           : [image.image_url for image in hotel.hotelimage_set.all()],
                'hotel_review_rate'     : float(hotel.review_set.all().aggregate(Avg('rate'))['rate__avg']) if hotel.review_set.all() else None,
                'room_type'             : [{
                    'image'          : room.image_url,
                    'room_name'      : room.name,
                    'original_price' : int(room.original_price),
                    'discount_price' : int(room.original_price * room.discount_rate),
                    'remain'         : room.reservationcheck_set.first().remain
                    }for room in hotel.room_set.all()]
                }

            return JsonResponse({'MESSAGE':'SUCCESS', 'results':results}, status=200)
        except ValueError:
            return JsonResponse({'MESSAGE':'VALUE_ERROR'}, status=400)
