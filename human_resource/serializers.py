
from rest_framework import serializers
from .models import *
from rest_framework import status
from rest_framework.response import Response

from django.contrib.auth import get_user_model


class EmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = '__all__'
        depth = 1


class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = '__all__'
        depth = 1


class AddressBookSerializer(serializers.ModelSerializer):
    class Meta:
        model = AddressBook
        fields = '__all__'


class BusinessAddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = BusinessAddress
        fields = '__all__'

class SupplierUserSerializer(serializers.ModelSerializer):
    class Meta:
        model=User
        fields=['id']

class SupplierSerializer(serializers.ModelSerializer):
    address = AddressBookSerializer(required=False, many=True, read_only=True)
    user = SupplierUserSerializer()

    class Meta:
        model = Supplier
        fields = ('name', 'address', 'user')
        depth = 2


class DeliveryAddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = DeliveryRegions
        fields = '__all__'
        depth = 1


class PickupStationsSerializer(serializers.ModelSerializer):
    class Meta:
        model = PickupStations
        fields = '__all__'
        depth = 1
