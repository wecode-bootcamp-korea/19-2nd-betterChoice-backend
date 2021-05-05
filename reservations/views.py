import json
import datetime
from django.http            import JsonResponse
from django.core.exceptions import ValidationError,ObjectDoesNotExist
from django.views           import View
from django.db              import transaction

from users.utils               import LoginDecorator
from reservations.models       import Reservation,Status
from hotels.models             import Room,ReservationCheck,Hotel
from users.models              import User

class ReservationView(View):
    @LoginDecorator
    def post(self,request):
        try:
            data = json.loads(request.body)
            user = request.user

            RESERVED = 1

            name         = data['name']
            phone_number = data['phone_number']
            check_in     = data['check_in']
            check_out    = data['check_out']
            status       = Status.objects.get(id=RESERVED)
            user         = User.objects.get(id=data['user'])
            hotel        = Hotel.objects.get(id=data['hotel'])
            room         = Room.objects.get(id=data['room'])

            if not name or not phone_number:
                return JsonResponse({'MESSAGE':'NO_INFORMATION'},status=404)

            with transaction.atomic():
                Reservation.objects.create (
                    name         = name,
                    phone_number = phone_number,
                    check_in     = check_in,
                    check_out    = check_out,
                    status       = status,
                    user         = user,
                    hotel        = hotel,
                    room         = room,
                )

            check_in_date = datetime.datetime.strptime(check_in, '%Y-%m-%d')
            check_out_date = datetime.datetime.strptime(check_out, '%Y-%m-%d')
            days = (check_out_date - check_in_date).days

            REMAIN = 0

            for use_day in range(days):
                reservation_remain = ReservationCheck.objects.get(room=room, date=check_in_date)
                if reservation_remain.remain == REMAIN:
                    return JsonResponse({"MESSAGE": "NO_REMAIN_ROOM"},status=404)
                else:
                    reservation_remain.remain -= 1
                    reservation_remain.save()
                    check_in_date = check_in_date + datetime.timedelta(days=1)

            return JsonResponse({'MESSAGE':'SUCCESS'}, status=200)

        except KeyError:
            return JsonResponse({'MESSAGE':'KEY_ERROR'},status=400)

        except ValidationError:
            return JsonResponse({'MESSAGE':'VALIDATION_ERROR'}, status=404)

        except Hotel.DoesNotExist:
            return JsonResponse({'MESSAGE':'NO_HOTEL'}, status=404)

        except Room.DoesNotExist:
            return JsonResponse({'MESSAGE':'NO_ROOM'}, status=404)

    @LoginDecorator
    def get(self,request):
        user_id = request.user
        reservations = Reservation.objects.filter(user=user_id)

        result = [{
                'name'         : reservation.name,
                'phone_number' : reservation.phone_number,
                'check_in'     : reservation.check_in,
                'check_out'    : reservation.check_out,
                'status'       : reservation.status.status,
                'hotel'        : reservation.hotel.name,
                'image_url'    : reservation.room.image_url,
                'price'        : int((reservation.check_out - reservation.check_in).days * (reservation.room.original_price * reservation.room.discount_rate)),
        }for reservation in reservations]

        return JsonResponse({'RESULTS': result},status=200)

    @LoginDecorator
    def patch(self,request):
        try:
            data = json.loads(request.body)

            CANCEL = 3

            reservation_id = data['id']
            check_in       = data['check_in']
            check_out      = data['check_out']
            room           = Room.objects.get(id=data['room'])

            status = Status.objects.get(id=CANCEL)
            Reservation.objects.filter(id=reservation_id).update(status=status)

            check_in_date = datetime.datetime.strptime(check_in, '%Y-%m-%d')
            check_out_date = datetime.datetime.strptime(check_out, '%Y-%m-%d')
            days = (check_out_date - check_in_date).days

            for cancel_day in range(days):
                reservation_remain = ReservationCheck.objects.get(room=room, date=check_in_date)
                if reservation_remain.remain == reservation_remain.quantity:
                    return JsonResponse({"MESSAGE": "INVALID_REMAIN"}, status=400)
                else:
                    reservation_remain.remain += 1
                    reservation_remain.save()
                    check_in_date = check_in_date + datetime.timedelta(days=1)

            return JsonResponse({"MESSAGE": "SUCCESS"}, status=200)

        except KeyError:
            return JsonResponse({"MESSAGE": "KEY_ERROR"}, status=400)

        except ValueError:
            return JsonResponse({"MESSAGE": "VALUE_ERROR"}, status=400)

        except Room.DoesNotExist:
            return JsonResponse({"MESSAGE":"NO_ROOM"},status=404)