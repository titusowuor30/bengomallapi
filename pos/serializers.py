from rest_framework import routers, serializers, viewsets
from .models import *
from django.contrib.auth import get_user_model


User = get_user_model()
# Serializers define the API representation.


class SalesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sales
        fields = '__all__'

class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = '__all__'


# Serializers define the API representation.


class SalesItemsSerializer(serializers.ModelSerializer):
    sale_id = SalesSerializer

    class Meta:
        model = salesItems
        fields = '__all__'
        depth = 2
