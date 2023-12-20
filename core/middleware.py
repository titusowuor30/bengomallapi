from django.utils import timezone
import json
import os
from django.http import HttpRequest
from django.contrib.sites.models import Site

class CoreMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        _,_=Site.objects.get_or_create(domain='https://www.yogisdelight.co.ke/login/',name='yogis main')
        request_data = {
        'HTTP_HOST':request.META.get('HTTP_HOST', 'localhost:8000'),
        'HTTP_X_FORWARDED_PROTO':request.META.get('HTTP_X_FORWARDED_PROTO', 'http'),
        'HTTP_REFERER':request.META.get('HTTP_REFERER', ''),
        'REMOTE_ADDR':request.META.get('REMOTE_ADDR', ''),
        'CSRF_COOKIE': request.META.get('CSRF_COOKIE',''),
        'REQUEST_URL': f'{request.scheme}://{request.get_host()}'
        }
        request_json = json.dumps(request_data)
        os.environ['REQUEST_DATA']=request_json
        data=os.environ.get('REQUEST_DATA')
        myrequest=HttpRequest()
        myrequest.META=data
        #print(myrequest.META)
        #user = request.user
        # if user.is_authenticated:
        #     #print(user.timezone)
        #     timezone.activate(user.timezone)
        # else:
        #     timezone.deactivate()  # Use the default timezone for anonymous users
        response = self.get_response(request)
        return response
