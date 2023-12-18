from django.shortcuts import render

# Create your views here.
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import permissions, authentication
from django.http import Http404
from .models import Cart
from .serializers import CartSerializer
from product.models import ProductSize, ProductColor
from django.contrib.auth import get_user_model


class CartList(APIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly,]

    def get(self, request):
        user_id=request.query_params.get('user_id', None)
        cartitems = Cart.objects.all()
        if user_id:
            cartitems=Cart.objects.filter(user__id=user_id)
        serializer = CartSerializer(cartitems, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = CartSerializer(data=request.data)
        print(request.data['stock'])
        if serializer.is_valid():
            stock = serializer.validated_data['stock']
            retail_price = serializer.validated_data.get('retail_price')

            # Check if the same product, size, and color already exist in the cart
            existing_cart_entry = Cart.objects.filter(
                user=serializer.validated_data['user'],
                stock=stock,
            ).first()

            if existing_cart_entry:
                # Update the existing cart entry with the new quantity
                existing_cart_entry.quantity += serializer.validated_data['quantity']
                existing_cart_entry.item_subtotal = existing_cart_entry.quantity * retail_price
                existing_cart_entry.item_total = existing_cart_entry.item_subtotal + existing_cart_entry.tax
                existing_cart_entry.save()
                icon="success"
                message="Item quantity updated successfully!"
                return Response({"icon":icon,"message":message}, status=status.HTTP_200_OK)
            else:
                # Create a new cart entry
                serializer.save()
                icon="success"
                message="Item added to cart successfully!"
                return Response({"icon":icon,"message":message}, status=status.HTTP_201_CREATED)
        return Response({"icon":"error","message":str(serializer.errors)}, status=status.HTTP_400_BAD_REQUEST)

class CartDetail(APIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly,]
    def get_object(self, pk):
        try:
            return Cart.objects.get(stock__id=pk)
        except Cart.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        cart = self.get_object(pk)
        serializer = CartSerializer(cart)
        return Response(serializer.data)

    def put(self, request, pk):
        cart = self.get_object(pk)
        serializer = CartSerializer(cart, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request,user_id=None,pk=None):
        if user_id !=0:
            message="Cart cleared!"
            Cart.objects.filter(user__id=user_id).delete()
        if pk !=0:
            cart = self.get_object(pk)
            cart.delete()
            message="Item removed from cart successfully!"
        return Response({"icon":"success","message":message},status=status.HTTP_200_OK)