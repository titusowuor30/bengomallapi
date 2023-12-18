
from django.urls import path, include
from rest_framework import routers
from .views import *
from .utils import *
# Routers provide an easy way of automatically determining the URL conf.
router = routers.DefaultRouter()
router.register('orders', OrderViewSet)
router.register('orderitems', OrderItemViewSet)
router.register('invoices', InvoicesViewSet)

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    path('', include(router.urls)),
    path('', include(router.urls)),
    path('oderlist/', oderlist),
    path('oerderadd/', save_order),
    path('orders/<int:id>/', delete_order),
    path('completeorder/<int:id>/<str:orderid>/', complete_order),
]
