
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



class Region(models.Model):
    name=models.CharField(max_length=150)
    pin_code = models.CharField(max_length=30)
    cod_avialble = models.BooleanField(default=False)
    delivery_avialble = models.BooleanField(default=True)
    delivery_charge  = models.FloatField(default=0.0)
    est_delivery_time = models.IntegerField(default=5)#in days    
    created_user = models.ForeignKey(settings.AUTH_USER_MODEL,related_name="region_created_user",on_delete=models.CASCADE)
    updated_user = models.ForeignKey(settings.AUTH_USER_MODEL,related_name="region_updated_user",on_delete=models.CASCADE)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField()
    
    def __str__(self) -> str:
        return self.name
    
    
    
class Designation(models.Model):
    designation=models.CharField(max_length=150)
    
    def __str__(self) -> str:
        return self.designation   
    
    
    
class Address(models.Model):
    ADDRESS_TYPE=(
        ("HOME","HOME"),
        ("OFFICE","OFFICE")
    )
    default=models.BooleanField(default=False)
    user=models.ForeignKey(settings.AUTH_USER_MODEL,related_name="user_address",on_delete=models.CASCADE)
    phone_number=models.CharField(max_length=20)
    name=models.CharField(max_length=150)
    type=models.CharField(choices=ADDRESS_TYPE,max_length=20,default="HOME")
    address=models.TextField()

    def __str__(self):
        return str(self.name)
    
    

class CustomUser(AbstractBaseUser, PermissionsMixin):
  
    email = models.EmailField(max_length=250, unique=True)
    name = models.CharField(max_length=30, blank=True, null=True)
   
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    phone=models.CharField(max_length=20,null=True,blank=True)
    date_joined = models.DateTimeField(default=datetime.now)
    designation=models.ForeignKey(Designation,related_name="designationField",on_delete=models.PROTECT,null=True)
    # permissions=models.ManyToManyField(UserRoles,related_name="permissionsFields")
 
    address = models.ManyToManyField(Address,related_name="user_address")

    

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = [ ]

    def __str__(self) -> str:
        return self.name


class Business(models.Model):
    name=models.CharField(max_length=150)
    logo=models.ImageField(upload_to='static/logos', blank=True, null=True)
    tax_number=models.CharField(max_length=50)
    address=models.TextField()
    email=models.EmailField()
    owner=models.ForeignKey(settings.AUTH_USER_MODEL,related_name="business_owner",on_delete=models.CASCADE)
    created_user=models.ForeignKey(settings.AUTH_USER_MODEL,related_name="creating_user_busines",on_delete=models.CASCADE)
    updated_user=models.ForeignKey(settings.AUTH_USER_MODEL,related_name="updating_user_business",on_delete=models.CASCADE)
    create_date=models.DateTimeField(auto_now_add=True)
    updated_date=models.DateField(default=datetime.now,null=True,blank=True)



class Category(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField()
    icon = models.ImageField(upload_to='static/category', blank=True, null=True)

    class Meta:
        ordering = ("name",)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Category, self).save(*args, **kwargs)


class SubCategory(models.Model):
    category = models.ForeignKey(Category, related_name='sub_category', on_delete=models.CASCADE)
    image= models.ImageField(upload_to='static/sub_category', blank=True, null=True)
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

class ProductImages(models.Model):
    is_vedio=models.URLField()
    image = models.ImageField(upload_to="static/products",null=True,blank=True)
    created_date = models.DateTimeField(auto_now_add=True)
    uploaded_user = models.ForeignKey(settings.AUTH_USER_MODEL,related_name="media_uploaded_user",on_delete=models.CASCADE)


class TaxModel(models.Model):
    tax_name = models.CharField(max_length=150,)
    tax_short_name = models.CharField(max_length=20,null=True,blank=True,default="-")
    created_user = models.ForeignKey(settings.AUTH_USER_MODEL,related_name="tax_created_user",on_delete=models.CASCADE)
    updated_user = models.ForeignKey(settings.AUTH_USER_MODEL,related_name="tax_updated_user",on_delete=models.CASCADE)
    created_date  = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField()
    
    
    def __str__(self) -> str:
        return self.tax_name
    
    
    

class Products(models.Model):
    
    region = models.ForeignKey(Region,related_name="product_regions",on_delete=models.CASCADE)
    business = models.ForeignKey(Business,related_name="product_business",on_delete=models.CASCADE)
    category = models.ForeignKey(SubCategory, related_name='products', on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    slug = models.SlugField()
    description = models.TextField(blank=True, null=True)
    market_price = models.PositiveIntegerField()
    selling_price = models.PositiveIntegerField()
    thumbnail = models.ImageField(upload_to='uploads/', blank=True, null=True)
    stock = models.IntegerField(default=0)
    pre_order = models.BooleanField(default=True)
    tax = models.ForeignKey(TaxModel,related_name="related_tax",on_delete=models.CASCADE)
     
    quantity_type = models.ForeignKey(QuantityVariant, blank=True, null=True, on_delete=models.PROTECT)
    color_type = models.ForeignKey(ColorVariant, blank=True, null=True, on_delete=models.PROTECT)
    size_type = models.ForeignKey(SizeVariant, blank=True, null=True, on_delete=models.PROTECT)
    date_added = models.DateTimeField(auto_now_add=True)
    images = models.ManyToManyField(ProductImages)
    created_user=models.ForeignKey(settings.AUTH_USER_MODEL,related_name="creating_user_product",on_delete=models.CASCADE)
    updated_user=models.ForeignKey(settings.AUTH_USER_MODEL,related_name="updating_user_product",on_delete=models.CASCADE)
    create_date=models.DateTimeField(auto_now_add=True)
    updated_date=models.DateField(default=datetime.now,null=True,blank=True)

    class Meta:
        ordering = ("-date_added",)

    def __str__(self):
        return self.name
    
    
    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Products, self).save(*args, **kwargs)





class Favourite(models.Model):
    product = models.ForeignKey(Products, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    isFavourite = models.BooleanField(default=False)

    def __str__(self):
        return f'ProductId ={self.product.id}user={self.user.username}|isFavourite={self.isFavourite}'


class CartProduct(models.Model):
    
    PRODUCT_STATUS=(
        ("ORDERD","ORDERD"),
        ("CANCELLED","CANCELLED"),
        ("PENDING","PENDING"),
        ("DELIVERD","DELIVERD")
        
    )
    product_status=models.CharField(choices=PRODUCT_STATUS,default="ORDERD",max_length=50)
    product = models.ForeignKey(Products,related_name="cart_product",on_delete=models.CASCADE)
    price = models.FloatField()
    quantity = models.PositiveIntegerField(default=1)
    subtotal = models.FloatField(default=0.0)

    def __str__(self):
        return f"Cart=={self.cart.id}<==>CartProduct:{self.id}==Quantity=={self.quantity}"


class Cart(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    
    total = models.FloatField()
    products = models.ManyToManyField(CartProduct)
    isComplete = models.BooleanField(default=False)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"User= {self.user.username}|isComplete={self.isComplete}"





class Order(models.Model):
    cart = models.OneToOneField(Cart, on_delete=models.CASCADE)
    address = models.ForeignKey(Address,on_delete=models.CASCADE,related_name="product_ordered_address")
    created_date = models.DateTimeField(auto_now_add=True)
    

    def __str__(self):
        return f"Cart=={self.cart.id}<==>phone:{self.phone}==address=={self.address}"
    
    
class PaymentModel(models.Model):
    transaction_id = models.CharField(max_length=350)
    user = models.ForeignKey(settings.AUTH_USER_MODEL,related_name="payment_user",on_delete=models.CASCADE)
    cart = models.ForeignKey(Cart,related_name="purchased_products",on_delete=models.CASCADE)
    created_date = models.DateTimeField(auto_now_add=True)
    

# class User(AbstractUser):
#     phone_regex = Regex

