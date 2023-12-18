
from django.urls import path, include
from rest_framework import routers
from .views import *

router = routers.DefaultRouter()
router.register('stock', InventoryViewSet)
router.register('pos_stock', PosInventoryViewSet)

urlpatterns = [
    path('', include(router.urls)),
    # path('add-product/', addProduct),
]
