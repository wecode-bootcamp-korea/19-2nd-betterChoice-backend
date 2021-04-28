from django.db import models

class Review(models.Model):
    content      = models.CharField(max_length = 45)
    rate         = models.DecimalField(max_digits = 4, decimal_places = 2)
    user         = models.ForeignKey('users.User', on_delete = models.CASCADE)
    hotel        = models.ForeignKey('hotels.Hotel', on_delete = models.CASCADE)
    reservation  = models.ForeignKey('reservations.Reservation', on_delete = models.CASCADE)
    created_at   = models.DateTimeField(auto_now_add = True)
    updated_at   = models.DateTimeField(auto_now = True)

    class Meta:
        db_table = 'reviews'

class ReviewComment(models.Model):
    review       = models.ForeignKey('Review', on_delete = models.CASCADE)
    comment      = models.CharField(max_length = 500)
    user         = models.ForeignKey('users.User', on_delete = models.CASCADE)
    created_at   = models.DateTimeField(auto_now_add = True)
    updated_at   = models.DateTimeField(auto_now = True)

    class Meta:
        db_table = 'review_comments'

class ReviewImage(models.Model):
    image_url    = models.CharField(max_length = 2000)
    review       = models.ForeignKey('Review', on_delete = models.CASCADE)

    class Meta:
        db_table = 'review_images'