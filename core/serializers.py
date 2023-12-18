from rest_framework import serializers
from .models import *

class FrontStoreSerializer(serializers.ModelSerializer):
    class Meta:
        model = FrontStore
        fields = '__all__'
        depth = 1
