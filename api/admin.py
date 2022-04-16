from ast import Add
from django.contrib import admin
from .models import *

admin.site.register(Products)
admin.site.register(Category)
admin.site.register(SubCategory)
admin.site.register(ColorVariant)
admin.site.register(QuantityVariant)
admin.site.register(SizeVariant)
admin.site.register(Cart)
admin.site.register(Favourite)
admin.site.register(Order)
admin.site.register(CartProduct)
admin.site.register(Designation)
admin.site.register(CustomUser)
admin.site.register(Address)