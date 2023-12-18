from django.utils import timezone
from rest_framework import viewsets, status
from django.db.models import Sum
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import AddressBook,Customer,Supplier,Employee,BusinessAddress
from django.shortcuts import render
from datetime import date, datetime, timedelta
from .models import *
from rest_framework.views import APIView
from rest_framework.response import Response
from pos.models import *
from django.http import Http404
from rest_framework.views import APIView
from rest_framework import viewsets
from rest_framework.decorators import api_view, permission_classes
from rest_framework import permissions, authentication
from django.db.models import Q, Count, Sum
from django.db.models.functions import Trunc
from rest_framework.decorators import action
from rest_framework.authtoken.models import Token
import json
from django.http import JsonResponse
from .serializers import *
from product.models import *
from order.models import *
from pos.models import *
from product.serializers import *
from authmanagement.serializers import UserSerializer
from stockinventory.models import StockInventory
from django.utils import timezone

class SupplierViewSet(APIView):
    queryset = Supplier.objects.all().prefetch_related(
        "address").select_related("user")
    serializer_class = SupplierSerializer
    permission_classes = [permissions.IsAuthenticated,]

    def get_object(self, pk):
        try:
            return Supplier.objects.get(pk=pk)
        except Supplier.DoesNotExist:
            raise Http404

    def get(self, request, format=None):
        context = []
        vendor = Vendor.objects.filter(user=request.user).first()
        if vendor != None:
            items = vendor.suppliers.all()
            for item in items:
                context.append(
                    {"id": item.id, "name": item.name, "user": item.user.id, "address": item.address.values("id", "state", "city","box","phone", "other_phone")})
        else:
            items = Supplier.objects.all()
            for item in items:
                context.append(
                    {"id": item.id, "name": item.name, "user": item.user.id, "address": item.address.values("id", "state", "city", "box","phone", "other_phone")})
        # print(context)
        return Response(context)

    def post(self, request, format=None):
        name = request.data['name']
        address = request.data['address']
        user, created = User.objects.get_or_create(
            username=str(name).replace(" ", "_"), first_name=name, last_name=name, email=f'{str(name).replace(" ", "_")}@gmail.com', password="@User123", is_active=True)
        # print(user, created)
        Token.objects.get_or_create(user=user)
        suplier, created = Supplier.objects.get_or_create(user=user, name=name)
        if suplier != None:
            for adr in address:
                suplier.address.add(adr)
            suplier.save()
            vendor = Vendor.objects.filter(user=request.user).first()
            if vendor != None:
                vendor.suppliers.add(suplier)
            vendor.save()
            return JsonResponse({"id": suplier.id, "name": suplier.name, "address": list(suplier.address.values("id", "state", "city", "box","phone", "other_phone", "default_address"))}, safe=False)
        return Response("Error", status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk, format=None):
        user = self.get_object(pk)
        serializer = UserSerializer(user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        user = self.get_object(pk)
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class CustomerViewSet(viewsets.ModelViewSet):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer
    permission_classes = [permissions.IsAuthenticated,]

    def get_object(self, pk):
        try:
            return Customer.objects.get(pk=pk)
        except Customer.DoesNotExist:
            raise Http404

    def get(self, request, format=None):
        context = []
        vendor = Vendor.objects.filter(user=request.user).first()
        if vendor != None:
            items = vendor.customers.all()
            for item in items:
                context.append(
                    {"id": item.id, "user": item.user, "address": list(item.addresses.values("id", "region", "city" "phone", "other_phone", "default_address"))})
        else:
            items = Customer.objects.all()
            for item in items:
                context.append(
                    {"id": item.id, "user": item.user, "address": list(item.address.values("id", "region", "city", "phone", "other_phone", "default_address"))})
        # print(context)
        return Response(context)

    def post(self, request, format=None):
        name = request.data['name']
        address = request.data['address']
        user, created = User.objects.get_or_create(
            username=str(name).replace(" ", "_"), first_name=name, last_name=name, email=f'{str(name).replace(" ", "_")}@gmail.com', password="@User123", is_active=True)
        # print(user, created)
        Token.objects.get_or_create(user=user)
        suplier, created = Customer.objects.get_or_create(user=user, name=name)
        if suplier != None:
            for adr in address:
                suplier.address.add(adr)
            suplier.save()
            vendor = Vendor.objects.filter(user=request.user).first()
            if vendor != None:
                vendor.suppliers.add(suplier)
            vendor.save()
            return JsonResponse({"id": suplier.id, "name": suplier.name, "address": list(suplier.address.values("id", "state", "city", "box", "phone", "other_phone"))}, safe=False)
        return Response("Error", status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk, format=None):
        user = self.get_object(pk)
        serializer = UserSerializer(user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        user = self.get_object(pk)
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class EmployeeViewSet(viewsets.ModelViewSet):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer
    permission_classes = [permissions.IsAuthenticated,]


class addressViewSet(viewsets.ModelViewSet):
    queryset = AddressBook.objects.all()
    serializer_class = AddressBookSerializer
    permission_classes = [permissions.IsAuthenticated,]

    def create(self, request, *args, **kwargs):
        # Map the incoming data to the expected format
        incoming_data = request.data
        customer_id = incoming_data.get('customer')
        region_name = incoming_data.get('region')
        city_name = incoming_data.get('city')
        # Retrieve or create Region and City objects based on names
        customer=Customer.objects.filter(user__id=customer_id).first()
        if region_name:
            region= DeliveryRegions.objects.filter(region__icontains=region_name).first()
        if city_name:
            city = PickupStations.objects.filter(pickup_location__icontains=city_name).first()
        # Create the address
        address_data = {
            "address_label": incoming_data.get('address_label'),
            "phone": incoming_data.get('phone'),
            "other_phone": incoming_data.get('other_phone'),
            "default_address": incoming_data.get('default_address'),
            "customer": customer.id,
            "region": region.id,
            "city": city.id,
        }
        if address_data['default_address']==True:
            default_addr=AddressBook.objects.filter(customer=customer,default_address=True).first()
            if default_addr:
                default_addr.default_address=False
                default_addr.save()

        serializer = AddressBookSerializer(data=address_data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        else:
            return Response(serializer.errors, status=400)

    def update(self, request, *args, **kwargs):
        # Get the address instance to update
        instance = self.get_object()

        # Map the incoming data to the expected format
        incoming_data = request.data
        customer_id = incoming_data.get('customer')
        region_name = incoming_data.get('region')
        city_name = incoming_data.get('city')

        # Retrieve or create Region and City objects based on names
        customer = Customer.objects.filter(user__id=customer_id).first()
        if region_name:
            region = DeliveryRegions.objects.filter(region__icontains=region_name).first()
        if city_name:
            city = PickupStations.objects.filter(pickup_location__icontains=city_name).first()

        # Create the updated address data
        address_data = {
            "address_label": incoming_data.get('address_label'),
            "phone": incoming_data.get('phone'),
            "other_phone": incoming_data.get('other_phone'),
            "default_address": incoming_data.get('default_address'),
            "customer": customer.id,
            "region": region.id if region else None,  # Use None if region is not specified
            "city": city.id if city else None,  # Use None if city is not specified
        }
        if address_data['default_address']==True:
            default_addr=AddressBook.objects.filter(customer=customer,default_address=True).first()
            default_addr.default_address=False
            default_addr.save()
        serializer = AddressBookSerializer(instance, data=address_data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class BusinessaddressViewSet(viewsets.ModelViewSet):
    queryset = BusinessAddress.objects.all()
    serializer_class = BusinessAddressSerializer
    permission_classes = [permissions.IsAuthenticated,]

class DeliveryRegionsViewSet(viewsets.ModelViewSet):
    queryset = DeliveryRegions.objects.all()
    serializer_class = DeliveryAddressSerializer
    permission_classes = [permissions.IsAuthenticated,]

    def get_queryset(self):
        queryset = super().get_queryset()
        # Apply filters based on query parameters
        region = self.request.query_params.get('region', None)
        if region != None:
            queryset = queryset.filter(region__icontains=region)
        return queryset


class PickupStationsViewSet(viewsets.ModelViewSet):
    queryset = PickupStations.objects.all()
    serializer_class = PickupStationsSerializer
    permission_classes = [permissions.IsAuthenticated,]

    def get_queryset(self):
        queryset = PickupStations.objects.all()
        # Filter by region ID if provided in the request
        region= self.request.query_params.get('region',None)
        if region:
            queryset = queryset.filter(region__region__icontains=region).values("id","open_hours","pickup_location","payment_options","description","helpline","shipping_charge")
        # Filter by pickup station ID if provided in the request
        region_id = self.request.query_params.get('id',None)
        if region_id:
            queryset = queryset.filter(region__id__in=region_id).values("id","open_hours","pickup_location","payment_options","description","helpline","shipping_charge")
        return queryset


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated,])
def top_buyers(request):
    vendor = Vendor.objects.filter(user=request.user).first()
    employee = Employee.objects.filter(user=request.user).first()
    if request.user.is_superuser:
        top_customers = Order.objects.annotate(
            total_spent=Sum('order_amount')).values('customer__user__pic', 'payment_status', 'customer__addresses__region', 'customer__user__first_name', 'customer__user__last_name', 'total_spent').filter(total_spent__gte=50).order_by('-total_spent').distinct()[:5]
    elif vendor != None:
        top_customers = Order.objects.filter(orderitems__product__vendor=vendor).annotate(
            total_spent=Sum('order_amount')).values('customer__user__pic', 'payment_status', 'customer__addresses__region', 'customer__user__first_name', 'customer__user__last_name', 'total_spent').filter(total_spent__gte=50).order_by('-total_spent').distinct()[:5]
    elif employee != None:
        employee = request.user.employee
        top_customers = Order.objects.filter(orderitems__product__vendor__employees=employee).annotate(
            total_spent=Sum('order_amount')).values('customer__user__pic',  'payment_status', 'customer__addresses__region', 'customer__user__first_name', 'customer__user__last_name', 'total_spent').filter(total_spent__gte=50).order_by('-total_spent').distinct()[:5]
    else:
        top_customers = ""
    return Response(list(top_customers))


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated,])
def top_products(request):
    vendor = Vendor.objects.filter(user=request.user).first()
    employee = Employee.objects.filter(user=request.user).first()
    if request.user.is_superuser:
        top_products = StockInventory.objects.annotate(total_sales=Sum('salesitems__qty')).filter(total_sales__gte=1).values(
            "sku", "product__title", "total_sales").order_by('-total_sales')[:5]
    elif vendor != None:
        top_products = StockInventory.objects.filter(vendor=vendor).annotate(total_sales=Sum('salesitems__qty')).filter(total_sales__gte=1).values(
            "sku", "product__title", "total_sales").order_by('-total_sales')[:5]
    elif employee != None:
        employee = request.user.employee
        top_products = StockInventory.objects.filter(vendor__employees=employee).annotate(total_sales=Sum('salesitems__qty')).filter(total_sales__gte=1).values(
            "sku", "product__title", "total_sales").order_by('-total_sales')[:5]
    else:
        top_products = ""
    return Response(list(top_products))


class SaleAnalyticsViewSet(viewsets.ViewSet):
    queryset = Products.objects.all()
    serializer_class = ProductsSerializer

    def list(self, request):
        sales_queryset=Sales.objects.filter(status='completed')
        # get vendor or vendor user
        vendor = Vendor.objects.filter(user=request.user).first()
        employee = Employee.objects.filter(user=request.user).first()
        # Get the selected filters
        filter = request.query_params.get('filter', 'Monthly')
        now = datetime.now()
        date = request.query_params.get('date', now.strftime('%Y-%m-%d'))
        # Determine the time interval for the selected filter
        if filter == 'Weekly':
            interval = 'day'
            start_date = datetime.strptime(date, '%Y-%m-%d').date() - timedelta(days=7)
        elif filter == 'Monthly':
            interval = 'week'
            start_date = datetime.strptime(date, '%Y-%m-%d').date().replace(day=1) - timedelta(days=1)
        elif filter == 'Yearly':
            interval = 'month'
            start_date = datetime.strptime(date, '%Y-%m-%d').date().replace(month=1, day=1) - timedelta(days=1)
         # Query the database to get the total sales for the selected period
        total_sales_current_period = sales_queryset.filter(date_added__gte=start_date, date_added__lte=date).aggregate(total__sum=Sum('grand_total'))['total__sum'] or 0
        # Query the database to get the total sales for the previous period
        total_sales_previous_period = sales_queryset.filter(date_added__gte=start_date - timedelta(days=1), date_added__lte=datetime.strptime(
            date, '%Y-%m-%d').date() - timedelta(days=1)).aggregate(total__sum=Sum('grand_total'))['total__sum'] or 0
        # print(total_sales_current_period)
        # print(total_sales_previous_period)

        # Calculate the sales growth rate
        if total_sales_previous_period == 0:
            sales_growth_rate = 100
        else:
            sales_diff = total_sales_current_period - total_sales_previous_period
            sales_growth_rate = round(
                (sales_diff / total_sales_previous_period) * 100, 2)

        # Query the database for the top 3 selling categories based on the selected filter
        top_categories = salesItems.objects.annotate(date=Trunc('date_added', interval)).values('stock__product__maincategory__categories__name', 'date').annotate(
            total=Sum('total')).values('stock__product__maincategory__categories__name', 'total').order_by('-total')
        if vendor != None:
            top_categories = top_categories.filter(stock__product__vendor=vendor)[:3]
        elif employee != None:
            top_categories = top_categories.filter(
                stock__product__vendor__employees=employee)[:3]
        else:
            top_categories = top_categories[:3]
        # Format the data into the desired format
        orders = Order.objects.annotate(date=Trunc(
            'created_at', interval)).values('order_id').annotate(order_count=Count('order_id')).order_by('created_at')
        customers = Customer.objects.annotate(date=Trunc(
            'user__date_joined', interval)).values("user__id").annotate(customer_coount=Count('user__id')).order_by('user__date_joined')
        data = []
        order_series = []
        customer_series = []
        customer_coount = Customer.objects.count()
        order_count = Order.objects.count()
        sales_count = salesItems.objects.count()
        conversion_ratio=0.00
        if customer_coount > 0:
           conversion_ratio = sales_count/customer_coount
        total_sales_amount = sales_queryset.aggregate(
            total=Sum('grand_total'))['total']
        for c in customers:
            customer_series.append(c['customer_coount'])
        for od in orders:
            order_series.append(od['order_count'])
        for category in top_categories:
            name = category['stock__product__maincategory__categories__name']
            sales_data = salesItems.objects.annotate(date=Trunc('date_added', interval)).values(
                'date').annotate(total=Sum('total')).filter(stock__product__maincategory__categories__name=name).order_by('date')
            # Create a list of total sales for each interval
            sales_list = []
            for sales in sales_data:
                sales_list.append(sales['total'])
            # Add the category and sales data to the result list
            for item in data:
                if item['name'] == name:
                    break
            else:
                data.append({'name': name, 'data': sales_list})
        data.append({"sales_amount": total_sales_amount,
                    "sales_count": sales_count, "conversion_ratio": conversion_ratio, "orders": order_count, "customers": customer_coount, "order_series": order_series, "customer_series": customer_series, "growth_rate": sales_growth_rate})
        return Response(list(data), status=status.HTTP_200_OK)
