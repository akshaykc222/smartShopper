from rest_framework import viewsets

from .serializer import *
from .models import *
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication


class CategoryView(APIView):
    permission_classes = [IsAuthenticated, ]
    authentication_classes = [TokenAuthentication, ]

    def get(self, request):
        queryset = SubCategory.objects.all()
        serializer = SubCategorySerializer(queryset, many=True)
        return Response({"Categories": serializer.data})


class SubCategoryView(APIView):
    permission_classes = [IsAuthenticated, ]
    authentication_classes = [TokenAuthentication, ]

    def get(self, request, pk):
        queryset = SubCategory.objects.filter(id=pk)
        serializer = SubCategorySerializer(queryset, many=True)
        return Response(serializer.data)


class ProductView(APIView):
    permission_classes = [IsAuthenticated, ]
    authentication_classes = [TokenAuthentication, ]

    def get(self, request, pk):
        query = Product.objects.filter(id=pk)
        data = []
        serializer_context = {
            'request': request,
        }

        serializer = ProductSerializer(query, many=True, context=serializer_context)
        for product in serializer.data:
            fab_query = Favourite.objects.filter(user=request.user).filter(product=product['id'])
            if fab_query:
                product['isFavourite'] = fab_query[0].isFavourite
            else:
                product['isFavourite'] = False
            data.append(product)
        return Response({"Products": data})


class FavouriteView(APIView):
    permission_classes = [IsAuthenticated, ]
    authentication_classes = [TokenAuthentication, ]

    def post(self, request):

        product = request.data["id"]
        try:
            product_obj = Product.objects.get(id=product)
            user = request.user
            single_favourite_product = Favourite.objects.filter(user=user).filter(product=product_obj).first()
            if single_favourite_product:
                print("single_favorit_product")
                ccc = single_favourite_product.isFavourite
                single_favourite_product.isFavourite = not ccc
                single_favourite_product.save()
            else:
                Favourite.objects.create(
                    product=product_obj, user=user, isFavourite=True)

            response_msg = {'error': False}

        except Exception as e:
            print("something went wrong " + str(e))
            response_msg = {'error': True}
        return Response(response_msg)


class RegisterView(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"error": False})
        return Response({"error": True})


class CartView(APIView):
    permission_classes = [IsAuthenticated, ]
    authentication_classes = [TokenAuthentication, ]

    def get(self, request):
        user = request.user
        data = []
        try:
            cart_obj = Cart.objects.filter(user=user).filter(isComplete=False)
            cart_serializer = CartSerializers(cart_obj, many=True)
            for cart in cart_serializer.data:
                cart_product_obj = CartProduct.objects.filter(cart=cart['id'])
                cart_product_serializer = CartProductSerializers(cart_product_obj, many=True)
                cart['cart_products'] = cart_product_serializer.data
                data.append(cart)
            response_msg = {'error': False, 'data': data}
        except Exception as e:
            print(e)
            response_msg = {'error': True, 'data': "no data"}

        return Response(response_msg)


class OrderView(APIView):
    permission_classes = [IsAuthenticated, ]
    authentication_classes = [TokenAuthentication, ]

    def get(self, request):
        try:
            query = Order.objects.filter(cart__user=request.user)
            serializer = OrdersSerializers(query, many=True)
            response_msg = {"error": False, "data": serializer.data}
        except:
            response_msg = {"error": True, "data": "no data"}
        return Response(response_msg)


class AddToCart(APIView):
    permission_classes = [IsAuthenticated, ]
    authentication_classes = [TokenAuthentication, ]

    def post(sefl, request):
        product_id = request.data['id']
        product_obj = Product.objects.get(id=product_id)
        # print(product_obj, "product_obj")
        cart_cart = Cart.objects.filter(
            user=request.user).filter(isComplit=False).first()
        cart_product_obj = CartProduct.objects.filter(
            product__id=product_id).first()

        try:
            if cart_cart:
                print(cart_cart)
                print("OLD CART")
                this_product_in_cart = cart_cart.cartproduct_set.filter(
                    product=product_obj)
                if this_product_in_cart.exists():
                    cartprod_uct = CartProduct.objects.filter(
                        product=product_obj).filter(cart__isComplit=False).first()
                    cartprod_uct.quantity += 1
                    cartprod_uct.subtotal += product_obj.selling_price
                    cartprod_uct.save()
                    cart_cart.total += product_obj.selling_price
                    cart_cart.save()
                else:
                    print("NEW CART PRODUCT CREATED--OLD CART")
                    cart_product_new = CartProduct.objects.create(
                        cart=cart_cart,
                        price=product_obj.selling_price,
                        quantity=1,
                        subtotal=product_obj.selling_price
                    )
                    cart_product_new.product.add(product_obj)
                    cart_cart.total += product_obj.selling_price
                    cart_cart.save()
            else:
                Cart.objects.create(user=request.user,
                                    total=0, isComplit=False)
                new_cart = Cart.objects.filter(
                    user=request.user).filter(isComplit=False).first()
                cart_product_new = CartProduct.objects.create(
                    cart=new_cart,
                    price=product_obj.selling_price,
                    quantity=1,
                    subtotal=product_obj.selling_price
                )
                cart_product_new.product.add(product_obj)
                new_cart.total += product_obj.selling_price
                new_cart.save()
            response_mesage = {
                'error': False, 'message': "Product add to card successfully", "productid": product_id}
        except:
            response_mesage = {'error': True,
                               'message': "Product Not add!Somthing is Wromg"}
        return Response(response_mesage)


class DeleteCarProduct(APIView):
    authentication_classes = [TokenAuthentication, ]
    permission_classes = [IsAuthenticated, ]

    def post(self, request):
        cart_product_id = request.data['id']
        try:
            cart_product_obj = CartProduct.objects.get(id=cart_product_id)
            cart_cart = Cart.objects.filter(
                user=request.user).filter(isComplit=False).first()
            cart_cart.total -= cart_product_obj.subtotal
            cart_product_obj.delete()
            cart_cart.save()
            response_msg = {'error': False}
        except:
            response_msg = {'error': True}
        return Response(response_msg)


class DeleteCart(APIView):
    permission_classes = [IsAuthenticated, ]
    authentication_classes = [TokenAuthentication, ]

    def post(self, request):
        cart_id = request.data['id']
        try:
            cart_obj = Cart.objects.get(id=cart_id)
            cart_obj.delete()
            response_msg = {'error': False}
        except:
            response_msg = {'error': True}
        return Response(response_msg)


class OrderCreate(APIView):
    permission_classes = [IsAuthenticated, ]
    authentication_classes = [TokenAuthentication, ]

    def post(self, request):
        try:
            data = request.data
            cart_id = data['cartid']
            address = data['address']
            email = data['email']
            phone = data['phone']
            cart_obj = Cart.objects.get(id=cart_id)
            cart_obj.isComplit = True
            cart_obj.save()
            Order.objects.create(
                cart=cart_obj,
                email=email,
                address=address,
                phone=phone,
            )
            response_msg = {"error": False, "message": "Your Order is Complit"}
        except:
            response_msg = {"error": True, "message": "Somthing is Wrong !"}
        return Response(response_msg)
