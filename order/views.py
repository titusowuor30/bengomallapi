from django.http import JsonResponse
from django.shortcuts import render
from datetime import date, datetime
from .models import *
from rest_framework.views import APIView
from rest_framework.response import Response
from pos.models import *
from django.http import Http404
from rest_framework.views import APIView
from rest_framework import viewsets
from rest_framework.decorators import api_view, permission_classes
from rest_framework import permissions, authentication
from rest_framework.decorators import action
from django.db.models import Q
from .serializers import *
from rest_framework.pagination import LimitOffsetPagination
from stockinventory.models import StockInventory
from human_resource.models import Customer


class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated,]
    pagination_class = LimitOffsetPagination  # Enable Limit and Offset Pagination

    def get_queryset(self):
        queryset = super().get_queryset()
        user = self.request.user
        vendor = Vendor.objects.filter(user=user).first()
        employee = Employee.objects.filter(user=user).first()
        customer=Customer.objects.filter(user=user).first()
        if vendor != None:
            queryset = queryset.filter(
                orderitems__stock__product__vendor=vendor)
        elif employee != None:
            employee = self.request.user.employee
            queryset = queryset.filter(
                orderitems__stock__product__vendor__employees=employee)
        elif customer !=None:
            queryset=queryset.filter(customer=customer)
        else:
            queryset=[]
        return queryset

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class OrderItemViewSet(viewsets.ModelViewSet):
    queryset = OrderItem.objects.all()
    serializer_class = OrderItemSerializer
    permission_classes = [permissions.IsAuthenticated,]
    pagination_class = LimitOffsetPagination  # Enable Limit and Offset Pagination

    def get_queryset(self):
        queryset = super().get_queryset()
       # Apply filters based on query parameters
        user = self.request.user

        vendor = Vendor.objects.filter(user=user).first()
        employee = Employee.objects.filter(user=user).first()
        if vendor != None:
            queryset = queryset.filter(stock__product__vendor=vendor)
        elif employee != None:
            employee = self.request.user.employee
            vendor = employee.vendor_set.first()
            queryset = queryset.filter(stock__product__vendor__employees=employee)
        else:
            queryset=[]
        return queryset

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class InvoicesViewSet(viewsets.ModelViewSet):
    queryset = Invoice.objects.all()
    serializer_class = InvoicesSerializer
    permission_classes = [permissions.IsAuthenticated,]
    pagination_class = LimitOffsetPagination  # Enable Limit and Offset Pagination

    def get_queryset(self):
        queryset = super().get_queryset()
       # Apply filters based on query parameters
        user = self.request.user
        vendor = Vendor.objects.filter(user=user).first()
        employee = Employee.objects.filter(user=user).first()
        if vendor != None:
            vendor_products = StockInventory.objects.filter(product__vendor=vendor).values('sku')
            order_items = OrderItem.objects.filter(stock__sku__in=vendor_products)
            # Get the invoices associated with the order items
            queryset = Invoice.objects.filter(
                order__orderitems__in=order_items)
        elif employee != None:
            # Get the logged-in employee user
            employee = self.request.user.employee
            # Get the products associated with the employee's vendor
            vendor = employee.vendor_set.first()
            vendor_products = Products.objects.filter(
                vendor__employees=employee)
            # Get the order items associated with the vendor products
            order_items = OrderItem.objects.filter(stock__product__in=vendor_products)
            # Get the invoices associated with the order items
            queryset = Invoice.objects.filter(
                order__orderitems__in=order_items)
        return queryset

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


