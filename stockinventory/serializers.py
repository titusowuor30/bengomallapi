
from rest_framework import serializers
from .models import *
from rest_framework import status
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from product.serializers import ProductsSerializer
from authmanagement.serializers import UserSerializer


class productSizeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductSize
        fields = ('id','size','unit','retail_price','unit_discount_price')
        depth=1

class productColorSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductColor
        fields = ('id','color')


class SupplierSerializer(serializers.ModelSerializer):
    class Meta:
        model = Supplier
        fields = ('name', 'address')
        depth=1


class StockSerializer(serializers.ModelSerializer):
    size=productSizeSerializer()
    color=productColorSerializer()
    product=ProductsSerializer()
    supplier=SupplierSerializer()
    class Meta:
        model = StockInventory
        fields = '__all__'
        depth=2

class ReviewsSerializer(serializers.ModelSerializer):
    user = UserSerializer

    class Meta:
        model = Review
        fields = ('text', 'rating', 'user')
        depth = 1
