from django.contrib.auth.models import Group
from authmanagement.models import MyUser
from django.utils import timezone


class SiteWideConfigs:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        roles=['admin','vendor','staff','manager','customer']
        for role in roles:
            role,created=Group.objects.get_or_create(name=role)
        if MyUser.objects.filter(email='admin@bengohub.co.ke').first() == None:
            admin=MyUser.objects.create(
                username='admin',
                email='admin@bengohub.co.ke',
                password='@Admin123',
                first_name='bengo',
                last_name='hub',
                phone='+254743793901',
                is_active=True,
                is_staff=True,
                is_superuser=True
            )
            admin.groups.add(Group.objects.get(name='admin'))
            admin.save()
        response = self.get_response(request)
        return response
