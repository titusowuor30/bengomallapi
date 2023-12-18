from rest_framework import serializers
from .models import (
    Vendor,Products,ProductImages,MainCategory,
    Category,Subcategory,ProductColor,ProductSize
    ,Favourites)
from rest_framework import status
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from vendor.serializers import VendoeSerializer
User = get_user_model()
# Serializers define the API representation.


class ImagesSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImages
        fields = ('image',)


#customproduct related serializers
class ProductVendorSerializer(serializers.ModelSerializer):
    class Meta:
        model=Vendor
        fields=('id','name')



class ProductsSerializer(serializers.ModelSerializer):
    vendor = ProductVendorSerializer()
    images = ImagesSerializer(many=True)

    class Meta:
        model = Products
        fields = '__all__'
        depth=3


class SubCategoriesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subcategory
        fields = ('id','name','display_image')


class CategoriesSerializer(serializers.ModelSerializer):
    subcategories = SubCategoriesSerializer(many=True, required=False)

    class Meta:
        model = Category
        fields =  ('id','name','display_image','subcategories')
        depth = 1


class MainCategoriesSerializer(serializers.ModelSerializer):
    categories=CategoriesSerializer(many=True,required=False)
    class Meta:
        model = MainCategory
        fields = ('id','name','display_image','categories')
        depth = 2


class productSizeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductSize
        fields = '__all__'

class productColorSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductColor
        fields = '__all__'


class FavouritesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Favourites
        fields = '__all__'
        depth = 1
