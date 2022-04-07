from django.shortcuts import render
from rest_framework.views import APIView
from smartShopper.api.models import *


# class CreateCategory(APIView):
#     def post(self, request):
#         request_user = request.user
#         cat_obj = Category.objects.create(name=request['name'], slug=request['slug'],im )
