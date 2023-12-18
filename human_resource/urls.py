
from django.urls import path, include
from rest_framework import routers
from .views import *

router = routers.DefaultRouter()
#router.register('suppliers', SupplierViewSet)
router.register('employees', EmployeeViewSet)
router.register('customers', CustomerViewSet)
router.register('addresses', addressViewSet)
router.register('businessaddress', BusinessaddressViewSet)
router.register('delivery_address', DeliveryRegionsViewSet)
router.register('pickup_stations', PickupStationsViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('top-products/', top_products),
    path('top-buyers/', top_buyers),
    path('sales-analytics/', SaleAnalyticsViewSet.as_view({'get': 'list'})),
    path('suppliers/', SupplierViewSet.as_view()),
    path('suppliers/<int:pk>/', SupplierViewSet.as_view()),
]
