from rest_framework import serializers
from .models import *
from rest_framework import status
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from human_resource.models import Customer
from product.models import *

User=get_user_model()

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model=User
        fields=['id','username','first_name','last_name']


class CustomerSerializer(serializers.ModelSerializer):
    user=UserSerializer()
    class Meta:
        model=Customer
        fields=['id','user']

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Products
        fields = ['title']


class SizeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductSize
        fields = ['size','unit']
        depth=1

class StockItemsSerializer(serializers.ModelSerializer):
    product=ProductSerializer(read_only=True)
    size=SizeSerializer(read_only=True)
    class Meta:
        model = StockInventory
        fields = ['size','product']
        depth=2

class OrderItemsSerializer(serializers.ModelSerializer):
    stock=StockItemsSerializer(read_only=True)
    class Meta:
        model = OrderItem
        fields = ['stock']

class OrderSerializer(serializers.ModelSerializer):
    customer = CustomerSerializer(required=False)
    orderitems = OrderItemsSerializer(many=True, read_only=True)

    class Meta:
        model = Order
        fields = '__all__'
        depth = 1

class OrdersSerializer(serializers.ModelSerializer):
    customer = CustomerSerializer(required=False)

    class Meta:
        model = Order
        fields = '__all__'
        depth = 1

class OrderItemSerializer(serializers.ModelSerializer):
    order = OrdersSerializer(required=False)

    class Meta:
        model = OrderItem
        fields = '__all__'
        depth = 1

class InvoicesSerializer(serializers.ModelSerializer):
    customer = CustomerSerializer(required=False)

    class Meta:
        model = Invoice
        fields = '__all__'
        depth = 1


