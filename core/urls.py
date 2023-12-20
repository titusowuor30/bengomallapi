
from django.urls import path,include
from rest_framework import routers
from .views import *

router = routers.DefaultRouter()
router.register('store', FrontStoreViewSet)
router.register('blog', BlogViewSet)


urlpatterns = [
path('', include(router.urls)),
]
