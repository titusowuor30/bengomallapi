from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import viewsets
from rest_framework.pagination import LimitOffsetPagination
from rest_framework import permissions, authentication
from .serializers import *
from .models import *

# Create your views here.
class FrontStoreViewSet(viewsets.ModelViewSet):
    queryset = FrontStore.objects.all().order_by('-flash_sale_end_date')
    serializer_class = FrontStoreSerializer
    authentication_classes = []
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    pagination_class = LimitOffsetPagination  # Use the custom pagination class

class BlogViewSet(viewsets.ModelViewSet):
    queryset = Blog.objects.all().order_by('-date_created')
    serializer_class = BlogSerializer
    authentication_classes = []
    permission_classes = []
    pagination_class = LimitOffsetPagination  # Use the custom pagination class
