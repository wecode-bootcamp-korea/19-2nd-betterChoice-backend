from django.db import models

class User(models.Model):
    email        = models.CharField(max_length = 45)
    password     = models.CharField(max_length = 500)
    nickname     = models.CharField(max_length = 45)
    phone_number = models.CharField(max_length = 45)
    is_social    = models.BooleanField()
    hotel        = models.ManyToManyField('hotels.Hotel', through = 'UserLike')
    coupon       = models.ManyToManyField('Coupon', through = 'UserCoupon')

    class Meta:
        db_table = 'users'

class UserCoupon(models.Model):
    coupon       = models.ForeignKey('Coupon', on_delete = models.SET_NULL, null = True)
    user         = models.ForeignKey('User', on_delete = models.CASCADE)
    is_coupon    = models.BooleanField()

    class Meta:
        db_table = 'user_coupons'

class Coupon(models.Model):
    name         = models.CharField(max_length = 45)

    class Meta:
        db_table = 'coupons'

class UserLike(models.Model):
    user         = models.ForeignKey('User', on_delete = models.CASCADE)
    hotel        = models.ForeignKey('hotels.Hotel', on_delete = models.CASCADE)
    is_like      = models.BooleanField()

    class Meta:
        db_table = 'user_likes'