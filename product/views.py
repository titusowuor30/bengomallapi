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
from stockinventory.serializers import ReviewsSerializer
from stockinventory.models import Review
from rest_framework.pagination import LimitOffsetPagination
from .functions import ExcelProductsImport

exceldata_import=ExcelProductsImport()

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Products.objects.filter(status=1).select_related(
        'vendor').prefetch_related('images')
    serializer_class = ProductsSerializer
    authentication_classes = []
    permission_classes = ()

    def get_queryset(self):
        queryset = super().get_queryset()
        search_item = self.request.query_params.get('filter', None)
        # Retrieve the limit and offset from the query string
        limit = self.request.query_params.get('limit')
        offset = self.request.query_params.get('offset')
        vendor = None
        user = self.request.user
        try:
            vendor = Vendor.objects.filter(user=user).first()
        except Exception as e:
            print(e)
        print(vendor)
        if search_item and not user.is_authenticated:
            queryset = queryset.filter(Q(maincategory__name__icontains=search_item) | Q(maincategory__categories__name__icontains=search_item))
        if user.is_authenticated:
            if search_item:
                maincategory_filter = Q(maincategory__name__icontains=search_item)
                categories_filter = Q(maincategory__categories__name__icontains=search_item)

                if vendor:
                    # Combine the maincategory and categories filters with the vendor filter
                    queryset = queryset.filter((maincategory_filter | categories_filter) & Q(vendor=vendor))
                else:
                    # If no vendor is specified, apply the maincategory and categories filters
                    queryset = queryset.filter(maincategory_filter | categories_filter)

        if limit is not None and offset is not None:
            # Apply pagination
            paginator = LimitOffsetPagination()
            paginated_queryset = paginator.paginate_queryset(queryset, self.request, view=self)

            return paginated_queryset

        return queryset

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        related_products = self.get_related_products(instance)
        serializer = self.get_serializer(instance)
        related_serializer = self.get_serializer(related_products, many=True)
        data = {
            "product": serializer.data,
            "related_products": related_serializer.data,
        }
        return Response(data)

    def get_related_products(self, product):
        """
        Returns a queryset of related products based on their titles, descriptions,
        categories, and subcategories using Q objects.
        """
        related_products = Products.objects.filter(
             Q(title__icontains=product.title)
            | Q(description__icontains=product.description)
            | Q(maincategory__categories__in=product.maincategory.categories.all())
        ).exclude(id=product.id).distinct()[:5]
        return related_products

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class ProductDetail(APIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly,]
    def get_object(self, pk):
        try:
            return Products.objects.get(pk=pk)
        except Products.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        cart = self.get_object(pk)
        serializer = ProductsSerializer(cart)
        return Response(serializer.data)

class ReviewsViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewsSerializer
    authentication_classes = []
    permission_classes = [permissions.IsAuthenticatedOrReadOnly,]

    def get_queryset(self):
        queryset = super().get_queryset()
        # Apply filters based on query parameters
        sku = self.request.query_params.get('sku', None)
        if sku is not None:
            queryset = queryset.filter(stock__sku=sku)
        return queryset

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

class MarkAsFavorite(APIView):
    permission_classes = (permissions.IsAuthenticated)
    authentication_classes = []
    def get(self, request):
        user = request.user  # Assuming you have authentication set up
        favorite_products = Favourites.objects.filter(user=user, is_favorite=True)
        serializer = FavouritesSerializer(favorite_products, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, pk=None):
        try:
            product = Products.objects.get(pk=pk)
            size=request.data.get('size')
            color=request.data.get('color')
            user = request.user  # Assuming you have authentication set up
            if product:
                favorite, created = Favourites.objects.get_or_create(user=user, product=product)
                favorite.is_favorite = True
                favorite.size=size
                favorite.color=color
                favorite.save()
            return Response({"message": "Product marked as a favorite"}, status=status.HTTP_200_OK)
        except Products.DoesNotExist:
            return Response({"error": "Product does not exist"}, status=status.HTTP_404_NOT_FOUND)

class Home(APIView):
    permission_classes = ([permissions.IsAuthenticatedOrReadOnly,])
    authentication_classes = ()

    def get(self, request, *args, **kwargs):
        now = datetime.now()
        current_year = now.year
        current_month = now.month
        current_day = now.day
        categories = len(Category.objects.all())
        subcategories = len(Subcategory.objects.all())
        products = len(Products.objects.all())
        transaction = len(Sales.objects.filter(
            date_added__year=current_year,
            date_added__month=current_month,
            date_added__day=current_day
        ))
        today_sales = Sales.objects.filter(
            date_added__year=current_year,
            date_added__month=current_month,
            date_added__day=current_day
        ).all()
        total_sales = sum(today_sales.values_list('grand_total', flat=True))
        context = {
            'categories': categories,
            'subcategories': subcategories,
            'products': products,
            'transaction': transaction,
            'total_sales': total_sales,
        }
        return Response(context)

class ToggleFavorite(APIView):
    def post(self, request, product_id):
        # Check if the user is authenticated
        if not request.user.is_authenticated:
            return Response({"error": "User not authenticated"}, status=status.HTTP_401_UNAUTHORIZED)

        # Check if the product with the given ID exists
        try:
            product = Products.objects.get(pk=product_id)
        except Products.DoesNotExist:
            return Response({"error": "Product not found"}, status=status.HTTP_404_NOT_FOUND)

        # Check if the product is already a favorite for the user
        favorite, created = Favourites.objects.get_or_create(user=request.user, product=product)
        favorite.is_favorite = not favorite.is_favorite
        favorite.save()

        return Response({"is_favorite": favorite.is_favorite}, status=status.HTTP_200_OK)

class LoadExcelProducts(APIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly,]

    def get(self, request,*args,**kwargs):
        vendor=Vendor.objects.filter(user=request.user).first()
        supplier = None
        if vendor:
            supplier =vendor.suppliers.first()
        exceldata_import.import_products_and_images(vendor,supplier)
        return Response("Products loaded successfully!")