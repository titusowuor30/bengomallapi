from rest_framework import serializers
from .models import Cart
from django.contrib.auth import get_user_model

User=get_user_model()

class CartUserSerializer(serializers.ModelSerializer):
    class Meta:
        model=User
        fields=['id']

class CartSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cart
        fields = '__all__'
