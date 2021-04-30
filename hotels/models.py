from django.db import models

class Category(models.Model):
    name         = models.CharField(max_length = 45)
    location     = models.ManyToManyField('Location', through = 'CategoryLocation')

    class Meta:
        db_table = 'categories'

class Location(models.Model):
    name         = models.CharField(max_length = 45)

    class Meta:
        db_table = 'locations'

class CategoryLocation(models.Model):
    category     = models.ForeignKey('Category', on_delete = models.CASCADE)
    location     = models.ForeignKey('Location', on_delete = models.CASCADE)

    class Meta:
        db_table = 'category_locations'

class Hotel(models.Model):
    name            = models.CharField(max_length = 45)
    address         = models.CharField(max_length = 500)
    thumbnail_image = models.URLField(max_length = 2000)
    longitude       = models.DecimalField(max_digits = 26, decimal_places = 20)
    latitude        = models.DecimalField(max_digits = 26, decimal_places = 20)
    category        = models.ForeignKey('Category', on_delete = models.CASCADE)
    location        = models.ForeignKey('Location', on_delete = models.SET_NULL, null = True)
    star            = models.IntegerField()

    class Meta:
        db_table    = 'hotels'

class HotelImage(models.Model):
    image_url    = models.URLField(max_length = 2000)
    hotel        = models.ForeignKey('Hotel', on_delete = models.CASCADE)

    class Meta:
        db_table = 'hotel_images'

class Room(models.Model):
    name            = models.CharField(max_length = 45)
    image_url       = models.URLField(max_length = 2000)
    original_price  = models.DecimalField(max_digits = 10, decimal_places = 2)
    discount_rate   = models.DecimalField(max_digits = 4, decimal_places = 2)
    occupancy       = models.IntegerField()
    hotel           = models.ForeignKey('Hotel', on_delete = models.CASCADE)

    class Meta:
        db_table    = 'rooms'

class ReservationCheck(models.Model):
    date         = models.DateField()
    quantity     = models.IntegerField()
    remain       = models.IntegerField()
    room         = models.ForeignKey('Room', on_delete = models.CASCADE)
    
    class Meta:
        db_table = 'reservation_checks'
