from django.contrib import admin
from .models import *

admin.site.register(Product)
admin.site.register(Category)
admin.site.register(SubCategory)
admin.site.register(ColorVariant)
admin.site.register(QuantityVariant)
admin.site.register(SizeVariant)
admin.site.register(Cart)
admin.site.register(Favourite)
admin.site.register(Order)
admin.site.register(CartProduct)
