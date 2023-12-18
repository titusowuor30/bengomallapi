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
from rest_framework.decorators import action
from django.db.models import Sum
from datetime import date

class TransactionViewSet(viewsets.ModelViewSet):
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer

    def perform_create(self, serializer):
        serializer.save()

    def perform_update(self, serializer):
        serializer.save()

    def perform_destroy(self, instance):
        instance.delete()

    def list(self, request, *args, **kwargs):
        queryset=super().get_queryset()
        # Get transactions by type (deposit/withdrawal)
        transaction_type = request.query_params.get('type', None)
        if transaction_type:
           queryset = queryset.filter(transactionType=transaction_type)
        # Get transactions by date
        fromdate = request.query_params.get('fromdate', None)
        todate = request.query_params.get('todate', None)
        if fromdate and todate:
           queryset = queryset.filter(date__range=[fromdate,todate])
        # Perform analytics for general deposit and withdrawal totals
        total_deposit =queryset.filter(transactionType='deposit').aggregate(total=Sum('amount'))['total']
        total_withdrawal = queryset.filter(transactionType='withdrawal').aggregate(total=Sum('amount'))['total']
        # Get the daily summary for deposits and withdrawals separately
        daily_summary_deposit = queryset.filter(date=date.today(), transactionType='deposit').aggregate(total=Sum('amount'))['total']
        daily_summary_withdrawal = queryset.filter(date=date.today(), transactionType='withdrawal').aggregate(total=Sum('amount'))['total']
        serializer = TransactionSerializer(queryset, many=True)

        return Response({
            'total_deposit': total_deposit or 0,
            'total_withdrawal': total_withdrawal or 0,
            'daily_summary': {
                "deposits":daily_summary_deposit or 0,
                "withdrawals":daily_summary_withdrawal or 0,
                },
            'transactions':serializer.data,
        })



@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated,])
def save_pos(request):
    # try:
    resp = {'title': 'failed', 'msg': ''}
    skus = request.data['sku']
    # sum(int(x) for x in list(request.data['total']))
    total = request.data['total']
    sub_total = request.data['sub_total']
    tax = request.data['tax']
    tax_amount = request.data['tax_amount']
    grand_total = request.data['grand_total']
    tendered_amount = request.data['tendered_amount']
    amount_change = request.data['change_amount']
    status = request.data['status']
    qty = request.data['qty']
    retail_price = request.data['retail_price']
    paymenthod = request.data['paymethod']
    paycode = request.data['paycode']
    print(skus)
    attendant = request.data['attendant']
    seller = Employee.objects.filter(user__id=attendant).first()
    # try:
    sale = Sales(attendant=seller, code=str(paycode), sub_total=sub_total, tax=tax, tax_amount=tax_amount,
                 grand_total=grand_total, tendered_amount=tendered_amount, amount_change=amount_change, paymethod=paymenthod, status=status)
    i = 0
    print(type(skus))
    if 'str' in str(type(skus)):
        skus = [skus]
    if 'str' in str(type(qty)):
        qty = [qty]
    if 'str' in str(type(retail_price)):
        retail_price = [retail_price]
    if 'str' in str(type(total)):
        total = [total]
    for sku in skus:
        print(sku)
        inventory = StockInventory.objects.get(sku=sku)
        if int(inventory.stock_level) < int(qty[i]):
            resp['title'] = 'Failed!'
            resp['icon'] = 'warning'
            resp['msg'] = f'<p>Product quantity selected exceeds stock units {inventory.stock_level}!<br/> Cannot complete sale!<br />Please consider restocking or select a lower quantity!</p>'
            return Response(resp)
        if inventory:
            sale.save()
            inventory.stock_level -= int(qty[i])
            inventory.save()
        salesItems(sale=sale, stock=inventory,
                   qty=qty[i], retail_price=retail_price[i], total=total[i]).save()
        i += 1
    resp['title'] = 'success'
    resp['icon'] = 'success'
    resp['msg'] = "Sales item saved!"
    # except Exception as e:
    #     resp['title'] = 'Error'
    #     resp['icon'] = 'error'
    #     resp['msg'] = str(e)
    #     print("Unexpected error:", e)
    return Response(resp)


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated,])
def salesList(request):
    offset = int(request.query_params.get('offset', 0))
    limit = int(request.query_params.get('limit', None))
    queryset=Sales.objects.values(
        "id", "code", "date_updated", "status", "paymethod", "grand_total")
    # Get transactions by type (deposit/withdrawal)
    status = request.query_params.get('status', None)
    if status:
        queryset = queryset.filter(status=status)
    # Get transactions by date
    fromdate = request.query_params.get('fromdate', None)
    todate = request.query_params.get('todate', None)
    if fromdate and todate:
        queryset = queryset.filter(created_at__range=[fromdate,todate])
    sales = queryset
    sales_data=[]
    for sale in sales:
        data = {}
        sale_items=[]
        # for field in sale._meta.get_fields(include_parents=False):
        #     if field.related_model is None:
        #         data[field.name] = getattr(sale, field.name)
        data["id"] = sale['id']
        data["code"] = sale['code']
        data["date"] = sale['date_updated']
        data["status"] = sale['status']
        data["paymethod"] = sale['paymethod']
        data["grand_total"] = sale["grand_total"]
        # items = []
        for item in salesItems.objects.filter(sale=sale['id']).values("id", "stock__sku","stock__product__title","qty", "retail_price", "total"):
            stock=StockInventory.objects.get(sku=item['stock__sku'])
            sale_items.append({"id": item['id'], "product_title":f"{item['stock__product__title']} {stock.size.size if stock.size else ''} {stock.size.unit.unit_symbol if stock.size else ''}",
                              "qty": item['qty'], "retail_price": item['retail_price'], "total": item['total']})
        data['sales_items']=sale_items
        sales_data.append(data)
        # data['items'] = items
        # print(sale_data)
    return Response(sales_data[offset:limit])


@api_view(['PUT', 'POST'])
@permission_classes([permissions.IsAuthenticated,])
def complete_sale(request, id, code):
    resp = {'status': 'failed', 'msg': ''}
    try:
        sales = Sales.objects.filter(id=id)
        for sale in sales:
            sale.code = code
            sale.status = 'completed'
            sale.save()
        resp['title'] = 'success'
        resp['icon'] = 'success'
        resp['msg'] = 'Sale has been completed!'
    except Exception as e:
        resp['title'] = 'Error'
        resp['icon'] = 'error'
        resp['msg'] = str(e)
        print("Unexpected error:", e)
    return Response(resp)


@api_view(['DELETE'])
@permission_classes([permissions.IsAuthenticated,])
def delete_sale(request, id):
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
