from django.contrib.auth import get_user_model
from rest_framework import serializers
from allauth.account.adapter import get_adapter
from allauth.utils import email_address_exists
from .models import *
from rest_framework.authtoken.models import Token
from django.contrib.auth.hashers import make_password
from allauth.account import app_settings as allauth_settings

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = "__all__"


class SubCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = SubCategory
        fields = "__all__"


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Products
        fields = "__all__"


class CartSerializers(serializers.ModelSerializer):
    class Meta:
        model = Cart
        fields = "__all__"


class CartProductSerializers(serializers.ModelSerializer):
    class Meta:
        model = CartProduct
        fields = "__all__"
        depth = 1


class OrdersSerializers(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = "__all__"
        depth = 1


class UserSerializer(serializers.ModelSerializer):
    User = get_user_model()

    class Meta:
        model = User
        fields = ('id', 'username', 'password',
                  'first_name', 'last_name', 'email',)
        extra_kwargs = {'password': {"write_only": True, 'required': True}}

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        Token.objects.create(user=user)
        return user


class DesignationSerializer(serializers.ModelSerializer):
    # created_user=serializers.PrimaryKeyRelatedField(read_only=True, default=serializers.CurrentUserDefault())
    # updated_user=serializers.PrimaryKeyRelatedField(read_only=True, default=serializers.CurrentUserDefault())
  
    class Meta:
        model=Designation
        fields='__all__'


class RegisterSerializer(serializers.Serializer):
    id=serializers.IntegerField(required=False, read_only=True)
    email = serializers.EmailField(required=allauth_settings.EMAIL_REQUIRED)
    name = serializers.CharField(required=True, write_only=True)
    phone = serializers.CharField(required=True, write_only=True)
    designation = serializers.PrimaryKeyRelatedField(queryset=Designation.objects.all())
    
    password1 = serializers.CharField(required=True, write_only=True)
    password2 = serializers.CharField(required=True, write_only=True)

    def validate_email(self, email):
        email = get_adapter().clean_email(email)
        if allauth_settings.UNIQUE_EMAIL:
            if email and email_address_exists(email):
                raise serializers.ValidationError(
                    {"error":"A user is already registered with this e-mail address."})
        return email

    def validate_password1(self, password):
        return get_adapter().clean_password(password)

    def validate(self, data):
        if data['password1'] != data['password2']:
            raise serializers.ValidationError(
                {"error":"The two password fields didn't match."})
        return data

    

    # def get_permissions_ids()

    def create(self, validated_data):
        validated_data.pop('password1')
        validated_data['password']= get_adapter().clean_password( validated_data.pop('password2'))
        
        # permissions=validated_data.pop('permissions')
        permission_ids=[]
        # for i in permissions:
        #     ui=UserRoles.objects.create(**i)
        #     permission_ids.append(ui)
        
        # permission_is
        user=CustomUser.objects.create(**validated_data)
        # user.permissions.set(permission_ids)
        return user

    def update(self, instance, validated_data):
        print("updatie i")
        validated_data['password']= get_adapter().clean_password( validated_data.pop('password2'))
  
     
        return super().update(instance, validated_data)
    # def to_representation(self, instance):
    #     data= super().to_representation(instance)
    #     try:
    #         data['designation']=DesignationSerializer(Designation.objects.get(id=data['designation'])).data
    #     except:
    #         print('not found')
    #     return data
    
class UserDetailsSerializer(serializers.ModelSerializer):
    designation = serializers.PrimaryKeyRelatedField(queryset=Designation.objects.all())
 
    class Meta:
        model = CustomUser
        fields = ('id', 'name', 'email', 'phone',
                  'designation', 'password','is_active')
        read_only_fields = ('email', )

    def to_representation(self, instance):
        data= super().to_representation(instance)
        print(data['designation'])

        try:
            data['designation']=DesignationSerializer(Designation.objects.get(id=data['designation'])).data
        except Exception as e:
            print(e)
      
        
        return data