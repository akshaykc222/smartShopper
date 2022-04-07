from django.db import models
from django.contrib.auth.models import AbstractUser, User


class ShopTypes(models.Model):
    type = models.TextField(max_length=100)

    def __str__(self):
        return self.type


class Shops(models.Model):
    user = models.ForeignKey(User, related_name='shops', on_delete=models.CASCADE)
    shop_name = models.TextField(max_length=200)
    created_date = models.DateField(auto_now_add=True)
    image = models.ImageField(upload_to='uploads/', blank=True, null=True)
    owner_name = models.TextField(max_length=200)
    type = models.ForeignKey(ShopTypes, blank=True, null=True, on_delete=models.CASCADE)
    isVerified = models.BooleanField(default=False)




