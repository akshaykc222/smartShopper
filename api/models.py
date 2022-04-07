from pyexpat import model
from django.contrib.auth.models import AbstractUser, User
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin 
from io import BytesIO
from PIL import Image
from smartShopper import settings
from django.core.files import File
from django.utils.text import slugify
from datetime import datetime
from api.custom_manager import CustomUserManager


class Designation(models.Model):
    designation=models.CharField(max_length=150)
    
    def __str__(self) -> str:
        return self.designation   


class CustomUser(AbstractBaseUser, PermissionsMixin):
  
    email = models.EmailField(max_length=250, unique=True)
    name = models.CharField(max_length=30, blank=True, null=True)
   
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    phone=models.CharField(max_length=20,null=True,blank=True)
    date_joined = models.DateTimeField(default=datetime.datetime.now)
    designation=models.ForeignKey(Designation,related_name="designationField",on_delete=models.PROTECT,null=True)
    # permissions=models.ManyToManyField(UserRoles,related_name="permissionsFields")
    birth_date = models.DateTimeField(blank=True, null=True)
    address = models.CharField(max_length=300,  blank=True, null=True)
    city = models.CharField(max_length=30, blank=True, null=True)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = [ ]

    def __str__(self) -> str:
        return self.name


class Business(models.Model):
    name=models.CharField(max_length=150)
    logo=models.ImageField(upload_to='uploads/', blank=True, null=True)
    tax_number=models.CharField(max_length=50)
    address=models.TextField()
    email=models.EmailField()
    owner=models.ForeignKey(settings.AUTH_USER_MODEL,related_name="business_owner",on_delete=models.CASCADE)
    created_user=models.ForeignKey(settings.AUTH_USER_MODEL,related_name="creating_user_busines",on_delete=models.CASCADE)
    updated_user=models.ForeignKey(settings.AUTH_USER_MODEL,related_name="updating_user_business",on_delete=models.CASCADE)
    create_date=models.DateTimeField(auto_now_add=True)
    updated_date=models.DateField(default=datetime.now,null=True,blank=True)

class Address(models.Model):
    ADDRESS_TYPE=(
        ("HOME","HOME"),
        ("OFFICE","OFFICE")
    )
    user=models.ForeignKey(settings.AUTH_USER_MODEL,related_name="user_address",on_delete=models.CASCADE)
    phone_number=models.CharField(max_length=20)
    name=models.CharField(max_length=150)
    type=models.CharField(choices=ADDRESS_TYPE,max_length=50,default="HOME")
    address=models.TextField()

class Category(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField()
    icon = models.ImageField(upload_to='uploads/', blank=True, null=True)

    class Meta:
        ordering = ("name",)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Category, self).save(*args, **kwargs)


class SubCategory(models.Model):
    category = models.ForeignKey(Category, related_name='sub_category', on_delete=models.CASCADE)
    image= models.ImageField(upload_to='uploads/', blank=True, null=True)
    name = models.CharField(max_length=200)
    slug = models.SlugField()

    class Meta:
        ordering = ("name",)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(SubCategory, self).save(*args, **kwargs)


class SizeVariant(models.Model):
    size_name = models.CharField(max_length=100)

    def __str__(self):
        return self.size_name


class QuantityVariant(models.Model):
    variant_name = models.CharField(max_length=100)

    def __str__(self):
        return self.variant_name


class ColorVariant(models.Model):
    color_name = models.CharField(max_length=100)
    color_code = models.CharField(max_length=100)

    def __str__(self):
        return self.color_name


class Products(models.Model):
    category = models.ForeignKey(SubCategory, related_name='products', on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    slug = models.SlugField()
    description = models.TextField(blank=True, null=True)
    market_price = models.PositiveIntegerField()
    selling_price = models.PositiveIntegerField()
    thumbnail = models.ImageField(upload_to='uploads/', blank=True, null=True)
    stock = models.IntegerField(default=5)
    quantity_type = models.ForeignKey(QuantityVariant, blank=True, null=True, on_delete=models.PROTECT)
    color_type = models.ForeignKey(ColorVariant, blank=True, null=True, on_delete=models.PROTECT)
    size_type = models.ForeignKey(SizeVariant, blank=True, null=True, on_delete=models.PROTECT)
    date_added = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ("-date_added",)

    def __str__(self):
        return self.name
    
    
    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Products, self).save(*args, **kwargs)


class ProductImages(models.Model):
    product = models.ForeignKey(Products, on_delete=models.PROTECT)
    image = models.ImageField(upload_to="uploads/")


class Favourite(models.Model):
    product = models.ForeignKey(Products, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    isFavourite = models.BooleanField(default=False)

    def __str__(self):
        return f'ProductId ={self.product.id}user={self.user.username}|isFavourite={self.isFavourite}'


class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    
    total = models.PositiveIntegerField()
    isComplete = models.BooleanField(default=False)
    date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"User= {self.user.username}|isComplete={self.isComplete}"


class CartProduct(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    product = models.ManyToManyField(Products)
    price = models.PositiveIntegerField()
    quantity = models.PositiveIntegerField()
    subtotal = models.PositiveIntegerField()

    def __str__(self):
        return f"Cart=={self.cart.id}<==>CartProduct:{self.id}==Quantity=={self.quantity}"


class Order(models.Model):
    cart = models.OneToOneField(Cart, on_delete=models.CASCADE)
    email = models.CharField(max_length=150)
    phone = models.CharField(max_length=20)
    address = models.CharField(max_length=200)

    def __str__(self):
        return f"Cart=={self.cart.id}<==>phone:{self.phone}==address=={self.address}"

# class User(AbstractUser):
#     phone_regex = Regex

