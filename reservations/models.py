from django.db import models

class Reservation(models.Model):
    name         = models.CharField(max_length = 45)
    phone_number = models.CharField(max_length = 45)
    check_in     = models.DateField()
    check_out    = models.DateField()
    status       = models.ForeignKey('Status', on_delete = models.SET_NULL, null = True)
    user         = models.ForeignKey('users.User', on_delete = models.CASCADE)
    hotel        = models.ForeignKey('hotels.Hotel', on_delete = models.SET_NULL, null = True)
    room         = models.ForeignKey('hotels.Room', on_delete = models.SET_NULL, null = True)
    created_at   = models.DateTimeField(auto_now_add = True)
    updated_at   = models.DateTimeField(auto_now = True)

    class Meta:
        db_table = 'reservations'

class Status(models.Model):
    status       = models.CharField(max_length = 45)

    class Meta:
        db_table = 'status'