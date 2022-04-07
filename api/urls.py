from django.urls import path
from .views import *
from rest_framework.authtoken.views import ObtainAuthToken

urlpatterns = [
    path('category/', CategoryView.as_view()),
    path('subcategory/<int:pk>/', SubCategoryView.as_view()),
    path('products/<int:pk>/', ProductView.as_view()),
    path('favourite/', FavouriteView.as_view()),
    path('login/', ObtainAuthToken.as_view()),
    path('register/', RegisterView.as_view()),
    path('cartItems/', CartView.as_view()),
    path('order/', CartView.as_view()),
]
