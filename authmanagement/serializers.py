from rest_framework import serializers
from rest_framework.authtoken.models import Token
from .models import *
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from rest_framework import status
from rest_framework.response import Response
from django.conf import settings
import os,json
from django.http import HttpRequest
import threading
from django.contrib.auth import get_user_model
from core.modules.custom_email_backend import BengomallEmailBackend


User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('groups', 'first_name', 'last_name',
                  'username', 'email','password','phone', 'pic', 'organisation')

    def create(self, validated_data):
        try:
            print(validated_data)
            user = User(
                first_name=validated_data['first_name'],
                last_name=validated_data['last_name'],
                email=validated_data['email'],
                phone=validated_data['phone'],
                pic=validated_data['pic'] if 'pic' in validated_data else 'user/default.png',
                organisation=validated_data['organisation'] if 'organisation' in validated_data else 'Bengo Mall',
                username=validated_data['username']
                )
            selectedroles = validated_data['groups'] if 'groups' in validated_data else None
            user.set_password(validated_data['password'])
            user.is_staff = False
            user.save()
            group,created=Group.objects.get_or_create(name='customer')
            print(group.id)
            user.is_active = False
            user.save()
            if selectedroles:
                roles = Group.objects.filter(name__in=selectedroles)
                for role in roles:
                    user.groups.add(role)
            else:
                user.groups.add(group)
            user.save()
            Token.objects.create(user=user)
            # Send confirmation email
            token = default_token_generator.make_token(user)
            user.email_confirm_token=token
            user.save()
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            print(uid,'\n',token)
            request=HttpRequest()
            reqdata=os.environ.get('REQUEST_DATA',{})
            print(reqdata)
            jsondata = json.loads(reqdata)
            request.META=jsondata
            subject = 'Confirm your registration'
            host = request.META['REQUEST_URL']
            message = render_to_string('authmanagement/confirm_email.html', {
                'host':host,
                'user': user,
                'uid': uid,
                'token': token,
            })
            # schedule in a thread
            email_thread = threading.Thread(target=BengomallEmailBackend(request,subject,message,[user.email,],[]).send_email,name='Email Thread')
            print("Starting email thread..")
            email_thread.start()
            print("Email thread started!")
        except Exception as e:
            user.delete()
            print("send mail error:{}".format(e))
        return user
