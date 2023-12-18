
from django.urls import path, include
from rest_framework import routers
from .views import *
from .reports.summary_reports import SalesSummaryReport
from .reports.inventory_reports import StockReports

router = routers.DefaultRouter()

router = routers.DefaultRouter()
router.register(r'transactions', TransactionViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('salesList/', salesList),
    path('salesadd/', save_pos),
    path('sales/<int:id>/', delete_sale),
    path('completesales/<int:id>/<str:code>/', complete_sale),
    #reporting urls
    path('sales/summary/',SalesSummaryReport.as_view(), name='sales_summary'),
    path('stock/summary/',StockReports.as_view(), name='stock_summary'),
]
