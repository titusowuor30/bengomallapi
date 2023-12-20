from http import client
from django.contrib.auth import authenticate,login
from .serializers import *
from rest_framework.authtoken.models import Token
from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.decorators import api_view, permission_classes
from rest_framework import viewsets
from rest_framework import permissions, authentication
from .models import *
from django.contrib.auth import logout
from .serializers import *
from .models import *
from vendor.models import Vendor
from human_resource.models import DeliveryRegions, PickupStations, AddressBook, Supplier, Customer
from json import JSONEncoder
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from rest_framework import status
from rest_framework.response import Response
from django.conf import settings
from django.core.mail.backends.smtp import EmailBackend
from django.core.mail import EmailMessage
from django.http import Http404
from django.contrib.sites.models import Site
from django.shortcuts import redirect
from django.contrib.auth import get_user_model

User = get_user_model()


class RegistrationView(generics.CreateAPIView):
    permission_classes = ()
    serializer_class = UserSerializer


class EmailConfirmView(APIView):
    user = None
    site_url = Site.objects.first()

    def get(self, request, uidb64, token):
        try:
            id = urlsafe_base64_decode(uidb64)
            print(id)
            user = User.objects.get(pk=id)
            print(token, '\n', user.email_confirm_token)
        except User.DoesNotExist:
            return Response({'error': 'Invalid token.'}, status=status.HTTP_400_BAD_REQUEST)
        if user != None and token == user.email_confirm_token:
            user.is_active = True
            print(user)
            user.save()
            return redirect(self.site_url.domain)
        return Response({'error': 'Invalid token.'}, status=status.HTTP_400_BAD_REQUEST)


class LogOutView(APIView):
    permission_classes = ()

    def post(self, request,):
        logout(request.user)
        return Response({"Logout Success!"}, status=status.HTTP_200_OK)


class LoginView(APIView):

    permission_classes = ()
    serializer_class = UserSerializer

    def post(self, request,):
        email = request.data.get('email')
        password = request.data.get('password')
        # print(request.data)
        addresses = {}
        user = authenticate(request,email=email, password=password)
        authuser=User.objects.filter(email=email,is_active=True).first()
        if authuser == None:
           return Response("Account inactive please confirm your email first!", status=status.HTTP_400_BAD_REQUEST)
        # try:
        vendor = Vendor.objects.filter(user=user).first()
        customer = Customer.objects.filter(user=user).first()
        supplier = Supplier.objects.filter(user=user).first()
        if customer:
           addresses['address'] = customer.addresses.values("id","customer__user__first_name","customer__user__last_name","phone","other_phone","postal_code","region__region","city__pickup_location","default_address","address_label")
        if supplier:
            addresses['address'] = supplier.address.values("id", "state",
                                                             "city", "box", "city", "street_or_road","phone", "other_phone")
        if vendor:
            addresses['address'] = vendor.address.values("id", "state",
                                                             "city", "box", "city", "street_or_road","phone", "other_phone")
        # except Exception as e:
        #     print(e)
        if user:
            login(request,user)
            token,created=Token.objects.get_or_create(user=user)
            return Response({"user": {"username": user.username, "email": user.email, "phone": user.phone,"pic":user.pic.url if user.pic else None, "fullname": user.first_name+" "+user.last_name, "id": user.id, "token": token.key}, 'addresses': addresses, "roles": [n['name'] for n in user.groups.values("name") if user.groups]})
        else:
            return Response("Wrong Credentials", status=status.HTTP_401_UNAUTHORIZED)


class UserViewSet(APIView):
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated,]

    def get_object(self, pk):
        try:
            return User.objects.get(pk=pk)
        except User.DoesNotExist:
            raise Http404

    def get(self, request, format=None):
        context = None
        if request.user.is_superuser:
            context = User.objects.values("username", "first_name", "last_name",
                                          "email", "phone", "groups__name", "organisation")
            # print(request.user.is_superuser)
        else:
            vendor = Vendor.objects.filter(user=request.user).first()
            # print(vendor)
            context = vendor.employees.values("user__username", "user__first_name", "user__last_name",
                                              "user__email", "user__phone", "user__groups__name", "user__organisation", "address",
                                              "national_id", "salary")
        context = list(context)
        return Response(context)

    def post(self, request, format=None):

        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

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
