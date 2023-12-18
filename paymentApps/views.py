from django.shortcuts import redirect, render
from django.http import HttpResponse
from django.http import JsonResponse
import requests
from django.db.models import Count, Sum
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
import json
from datetime import date, datetime
from django.contrib.auth import get_user_model
from django.http import JsonResponse
from django.shortcuts import render
from datetime import date, datetime
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import *
from order.models import *
from pos.models import *
from django.http import Http404
from rest_framework.views import APIView
from rest_framework import viewsets
from rest_framework.decorators import api_view, permission_classes
from rest_framework import permissions, authentication
import random
import time
import datetime
import asyncio
import aiohttp
from requests.auth import HTTPBasicAuth
from . mpesa_credentials import MpesaAccessToken, LipanaMpesaPpassword


@api_view(['GET', 'POST'])
@permission_classes([permissions.IsAuthenticated,])
def getAccessToken(request):
    consumer_key = 'pl1iuAP0UJTg7iHSGWsuTwKNBXcAbZCU'
    consumer_secret = 'BUzDTBeGOO0P8HMn'
    api_URL = 'https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials'
    r = requests.get(api_URL, auth=HTTPBasicAuth(
        consumer_key, consumer_secret))
    mpesa_access_token = json.loads(r.text)
    validated_mpesa_access_token = mpesa_access_token['access_token']

    return HttpResponse(validated_mpesa_access_token)


async def make_request(url, headers, payload):
    async with aiohttp.ClientSession() as session:
        async with session.post(url, json=payload, headers=headers) as response:
            return await response.text()


@api_view(['GET', 'POST'])
@permission_classes([permissions.IsAuthenticated,])
def stk_push(request):
    data = {}
    body = request.data
    print(body)
    # request.body.decode('utf-8')
    # body = json.loads(body)
    access_token = MpesaAccessToken.validated_mpesa_access_token
    shortcode = LipanaMpesaPpassword.Business_short_code
    pwd = LipanaMpesaPpassword.decode_password
    timestamp = LipanaMpesaPpassword.lipa_time
    amount = float(body['total'])
    stkpush_url = "https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest"
    headers = {"Authorization": "Bearer %s" % access_token}
    request = {
        "BusinessShortCode": shortcode,
        "Password": pwd,
        "Timestamp": timestamp,
        "TransactionType": "CustomerPayBillOnline",
        "Amount": 1,
        "PartyA": body['phone'],
        "PartyB": shortcode,
        "PhoneNumber": body['phone'],
        "CallBackURL": "https://459e-154-159-237-83.ngrok-free.app/callback/",
        "AccountReference": "Bengo POS %s" % body['reference'],
        "TransactionDesc": "Bengo POS %s" % body['tr_description']
    }
    r = requests.post(stkpush_url, json=request, headers=headers)
    resp = json.loads(r.text.strip())
    data['checkoutID'] = resp['CheckoutRequestID']
    data['password'] = pwd
    data['timestamp'] = timestamp
    # save transaction details
    Transactions.objects.create(
        orderid=body['orderId'], checkoutid=resp['CheckoutRequestID'], timestamp=timestamp, secret=pwd, status='pending')
    data['response'] = resp
    time.sleep(10)
    return Response(data)

@api_view(['GET', 'POST'])
@permission_classes([permissions.IsAuthenticated,])
def confirm_payment(request):
    try:
        time.sleep(5)
        pwd = request.data['pwd']
        timestamp = request.data['timestamp']
        checkout_id = request.data['chekoutID']
        orderid = request.data['orderId']
        url = "https://sandbox.safaricom.co.ke/mpesa/stkpushquery/v1/query"
        # Set up the headers with the access token
        token = MpesaAccessToken.validated_mpesa_access_token
        headers = {"Authorization": "Bearer %s" %
                   token, "Content-Type": "application/json"}
        # Set up the payload with the transaction code
        payload = {
            "BusinessShortCode": LipanaMpesaPpassword.Business_short_code,
            "Password": pwd,
            "Timestamp": timestamp,
            "CheckoutRequestID": checkout_id
        }
        # Make the GET request
        resp = requests.post(url, headers=headers, json=payload)
        resp = json.loads(resp.text.strip())
        resultcode = int(resp['ResultCode'])
        tr = Transactions.objects.get(orderid=orderid)
        if resultcode == 0:
            # get order details
            invoice = Invoice.objects.get(invoice_id=orderid)
            order = Order.objects.get(order_id=orderid)
            sale = Sales.objects.get(code=orderid)
            delivery = Deliveries.objects.get(order=order)
            delivery.delivery_from_date = datetime.datetime.now()+datetime.timedelta(days=7)
            delivery.delivery_to_date = datetime.datetime.now()+datetime.timedelta(days=10)
            invoice.status = 'paid'
            invoice.updated_at = datetime.datetime.now()
            order.confirm_status = 'confirmed'
            sale.status = 'complete'
            invoice.save()
            order.save()
            sale.save()
            delivery.save()
            # update transaction
            tr.status = 'success'
        tr.status = 'canceled'
        tr.save()
        resp['title'] = 'Success'
        resp['icon'] = 'success'
        resp['msg'] = str(resp['ResultDesc'])
        resp = resp['ResultDesc']
        return Response(resp)
    except Exception as e:
        resp['title'] = 'Error'
        resp['icon'] = 'error'
        resp['msg'] = str(e)
        resp = resp['ResultDesc'] = "Error submitting transaction!"


@api_view(['GET', 'POST'])
def MpesaCallBack(request):
    try:
        data = request.body.decode('utf-8')
        mpesa_payment = json.loads(data)
        log_file = "Mpesastkresponse.json"
        with open(log_file, "a") as log:
             json.dump(mpesa_payment, log)
        print("callback sent:"+str(data))
        print(mpesa_payment)
        print(mpesa_payment)
        result = 0
        stk_res = mpesa_payment['Body']['stkCallback']
        # if result == stk_res['ResultCode']:
        #     SubmitToDB(request)
        return Response(stk_res)
    except Exception as e:
        print(e)


# def send_email(subject, message, receivers=[]):
#     print(settings.EMAIL_HOST_USER)
#     try:
#         send_mail(
#             subject,
#             message,
#             settings.EMAIL_HOST_USER,
#             receivers,
#             fail_silently=False,
#         )
#         print('Mail Sent')
#     except Exception as e:
#         print("mail:"+e)

# function for sending SMS


# def sendSMS(msghead, message):
#     # 'test_gshuPaZoeEG6ovbc8M79w0QyM'  # xkMHWtkM2FBlxjYmbnc91u1la #307yPiT7RKFdqMLto2ObUn8A7
#     ACCESS_KEY = 'btUcmsEbzKaaqQlTBTeZHfAaQ'  # settings.MESSAGE_BIRD_TEST_API_KEY
#     print(ACCESS_KEY)
#     try:
#         # Create a MessageBird client with the specified ACCESS_KEY.
#         client = messagebird.Client(ACCESS_KEY)
#         # Send a new message.
#         print(msghead)
#         print(message)
#         number = settings.TEL
#         print(settings.TEL)
#         msg = client.message_create(
#             'WMS Center',
#             '+254743793901',
#             'New Invoice Generated please login to Waste Management System and check it',
#             {'reference': 'Foobar'}
#         )
#         # Print the object information.
#         print('\nThe following information was returned as a Message object:\n')
#         print('  id                : %s' % msg.id)
#         print('  href              : %s' % msg.href)
#         print('  direction         : %s' % msg.direction)
#         print('  type              : %s' % msg.type)
#         print('  originator        : %s' % msg.originator)
#         print('  body              : %s' % msg.body)
#         print('  reference         : %s' % msg.reference)
#         print('  validity          : %s' % msg.validity)
#         print('  gateway           : %s' % msg.gateway)
#         print('  typeDetails       : %s' % msg.typeDetails)
#         print('  datacoding        : %s' % msg.datacoding)
#         print('  mclass            : %s' % msg.mclass)
#         print('  scheduledDatetime : %s' % msg.scheduledDatetime)
#         print('  createdDatetime   : %s' % msg.createdDatetime)
#         print('  recipients        : %s\n' % msg.recipients)
#         print('Message Sent!')
#         print()
#     except messagebird.client.ErrorException as e:
#         print('\nAn error occured while requesting a Message object:\n')

#         for error in e.errors:
#             print('  code        : %d' % error.code)
#             print('  description : %s' % error.description)
#             print('  parameter   : %s\n' % error.parameter)
