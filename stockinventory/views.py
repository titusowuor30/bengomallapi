from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import *
from django.shortcuts import render
from datetime import date, datetime
from .models import Products,StockInventory
from vendor.models import Vendor
from rest_framework.views import APIView
from rest_framework.response import Response
from django.http import Http404
from rest_framework.views import APIView
from rest_framework import viewsets
from rest_framework.decorators import api_view, permission_classes
from rest_framework import permissions, authentication
from .serializers import *
from django.db.models import Q,Sum
from django.db.models import F, ExpressionWrapper, DecimalField
from rest_framework.pagination import LimitOffsetPagination
# Create your views here.


class InventoryViewSet(viewsets.ModelViewSet):
    queryset = StockInventory.objects.all()
    serializer_class = StockSerializer
    authentication_classes = []
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    pagination_class = LimitOffsetPagination  # Use the custom pagination class

    def get_queryset(self):
        queryset = super().get_queryset()
        limit = self.request.query_params.get('limit', 8)
        offset = self.request.query_params.get('offset', 0)
        prod_id = self.request.query_params.get('prod_id', None)
        search_item = self.request.query_params.get('filter', None)
        vendor = None
        user = self.request.user

        try:
            vendor = Vendor.objects.filter(user=user).first()
        except Exception as e:
            print(e)

        if search_item and not user.is_authenticated:
            queryset = queryset.filter(
                Q(product__maincategory__name__icontains=search_item) |
                Q(product__maincategory__categories__name__icontains=search_item)
            ).distinct()

        if user.is_authenticated:
            if search_item:
                maincategory_filter = Q(
                    product__maincategory__name__icontains=search_item)
                categories_filter = Q(
                    product__maincategory__categories__name__icontains=search_item)

                if vendor:
                    queryset = queryset.filter(
                        (maincategory_filter | categories_filter) & Q(
                            product__vendor=vendor)
                    ).distinct()
                else:
                    queryset = queryset.filter(
                        maincategory_filter | categories_filter).distinct()

            if prod_id:
                product = Products.objects.filter(id=prod_id).first()
                queryset = queryset.filter(product=product).distinct()
        return queryset

class PosInventoryViewSet(viewsets.ModelViewSet):
    queryset = StockInventory.objects.filter(stock_level__gt=0)
    serializer_class = StockSerializer
    authentication_classes = []
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    pagination_class = LimitOffsetPagination  # Use the custom pagination class

    def get_queryset(self):
        queryset = super().get_queryset()
        search_item = self.request.query_params.get('filter', None)

        # Create a Q object to filter products by maincategory and categories
        if search_item:
            maincategory_filter = Q(product__maincategory__name__icontains=search_item)
            categories_filter = Q(product__maincategory__categories__name__icontains=search_item)
            sku_filter = Q(sku__icontains=search_item)
            id_filter = Q(id__icontains=search_item)
            serial_filter = Q(serial__icontains=search_item)
            title_filter = Q(product__title__icontains=search_item)
            queryset = queryset.filter(maincategory_filter|categories_filter|sku_filter|id_filter|serial_filter|title_filter).distinct()
        return queryset