from pickle import FALSE
from django.shortcuts import redirect, render
from django.http import HttpResponse
from flask import jsonify
from product.models import *
from django.db.models import Count, Sum
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
import json
import sys
from datetime import date, datetime
from django.contrib.auth import get_user_model
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
from .serializers import *
import random
import time
from stockinventory.models import StockInventory
from cart.models import Cart
from human_resource.models import PickupStations
# Create your views here.


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated,])
def save_order(request):
    try:
        resp = {'title': 'failed', 'msg': ''}
        orderitems = json.loads(request.data['orderitems'])
        print(orderitems)
        sub_total = request.data['subtotal']
        tax_amount = request.data['tax_amount']
        total = request.data['total']
        paymenthod = request.data['paymethod']
        orderId = request.data['orderId']
        userid = request.data['userid']
        status = request.data['status']
        address_id = request.data['address_id']
        address=PickupStations.objects.get(id=address_id)
        customer = Customer.objects.get(user=userid)
        # add sales
        sale = Sales(code=str(orderId), sub_total=sub_total, tax_amount=tax_amount,
                     grand_total=total, tendered_amount=total, amount_change=0, paymethod=paymenthod, status=status, sales_type="online")
        # add order
        order = Order(customer=customer, order_id=orderId,delivery_address=address,
                      order_amount=total, confirm_status=status, dispatch_status='pending')
        # add invoice
        invoice = Invoice(customer=customer, invoice_id=orderId,
                          amount=total, status='pending')
        for item in orderitems:
            quantity = int(item['quantity'])
            stock = StockInventory.objects.get(id=item['stock_id'])
            sale.tax = item['tax']
            if int(stock.stock_level) < int(quantity):
                resp['title'] = 'Failed!'
                resp['icon'] = 'warning'
                resp['msg'] = 'Product quantity selected exceeds stock units! Cannot complete sale!'
                return Response(resp)
            sale.save()
            order.save()
            invoice.order=order
            invoice.save()
            stock.stock_level -= int(quantity)
            stock.save()
            #address= PickupStations.objects.get(id=int(address_id))
            salesItems(sale=sale, stock=stock,
                       qty=quantity, retail_price=int(item['item_subtotal']), total=int(item['item_total'])).save()
            OrderItem(order=order, stock=stock,
                      quantity=quantity, retail_price=int(item['item_subtotal']), total=int(item['item_total'])).save()
            Cart.objects.filter(user__id=userid).delete()
        resp['title'] = 'success'
        resp['icon'] = 'success'
        resp['msg'] = "Your order has been placed!\nThank you for shopping with Bengomall!"
    except Exception as e:
        resp['title'] = 'Error'
        resp['icon'] = 'error'
        resp['msg'] = str(e)
        print("Unexpected error:", e)
    return Response(resp)


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated,])
def oderlist(request):
    orders = Order.objects.values(
        "id", "order_id", "date_updated", "status", "paymethod", "order_amount")
    order_data = []
    for order in orders:
        data = {}
        data["id"] = order['id']
        data["order_id"] = order['order_id']
        data["date"] = order['created_at']
        data["status"] = order['status']
        data["order_amount"] = order["order_amount"]
        # items = []
        for item in OrderItem.objects.filter(order_id=order['id']).values("id", "product__sku", "product__title", "qty", "retail_price", "total"):
            order_data.append({"sales_details": data, "id": item['id'], "sku": item['product__sku'], "product_title": item['product__title'],
                              "qty": item['qty'], "retail_price": item['retail_price'], "total": item['total']})
    return Response(order_data)


@api_view(['PUT', 'POST'])
@permission_classes([permissions.IsAuthenticated,])
def complete_order(request, id, orde_id):
    resp = {'status': 'failed', 'msg': ''}
    try:
        orders = Order.objects.filter(id=id)
        for order in orders:
            order.order_id = orde_id
            order.status = 'completed'
            order.save()
        resp['title'] = 'success'
        resp['icon'] = 'success'
        resp['msg'] = 'Order has been completed!'
    except Exception as e:
        resp['title'] = 'Error'
        resp['icon'] = 'error'
        resp['msg'] = str(e)
        print("Unexpected error:", e)
    return Response(resp)


@api_view(['DELETE'])
@permission_classes([permissions.IsAuthenticated,])
def delete_order(request, id):
    resp = {'status': 'failed', 'msg': ''}
    try:
        Sales.objects.filter(id=id).delete()
        resp['title'] = 'success'
        resp['icon'] = 'success'
        resp['msg'] = 'Sale Record has been deleted.'
    except Exception as e:
        resp['title'] = 'Error'
        resp['icon'] = 'error'
        resp['msg'] = str(e)
        print("Unexpected error:", sys.exc_info()[0])
    return Response(resp)
