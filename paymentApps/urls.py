
from django.urls import path, include
from rest_framework import routers
from .views import *
# Routers provide an easy way of automatically determining the URL conf.
router = routers.DefaultRouter()

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    path('', include(router.urls)),
    path('mpesaAuth/', getAccessToken),
    path('stkpush/', stk_push),
    path('callback/', MpesaCallBack),
    path('payment/confirm/', confirm_payment),
]
