from django.db.models import Sum, Count
from django.db.models import Q
from rest_framework.views import APIView
from rest_framework.response import Response
from pos.serializers import SalesSerializer,SalesItemsSerializer
from pos.models import Sales,salesItems
from django.utils import timezone
from datetime import timedelta

class SalesSummaryReport(APIView):
    def get(self, request, *args, **kwargs):
        # Date range parameters
        start_date = request.query_params.get('start_date', None)
        end_date = request.query_params.get('end_date', None)
        report_type = request.query_params.get('report_type', 'daily')

        # Default to today for start_date if not provided
        if not start_date:
            start_date = timezone.now().date()

        # Default to today for end_date if not provided
        if not end_date:
            end_date = timezone.now().date()

        # Choose the report type
        if report_type == 'daily':
            # Daily Sales Summary
            sales_data = Sales.objects.filter(date_added__date=start_date)
        elif report_type == 'weekly':
            # Weekly Sales Summary
            week_start = start_date - timedelta(days=start_date.weekday())
            week_end = week_start + timedelta(days=6)
            sales_data = Sales.objects.filter(date_added__date__range=[week_start, week_end])
        elif report_type == 'monthly':
            # Monthly Sales Summary
            sales_data = Sales.objects.filter(date_added__year=start_date.year, date_added__month=start_date.month)
        elif report_type == 'yearly':
            # Yearly Sales Summary
            sales_data = Sales.objects.filter(date_added__year=start_date.year)
        elif report_type == 'custom':
            # Custom Date range Sales Summary
            sales_data = Sales.objects.filter(date_added__date__range=[start_date, end_date])
        else:
            return Response({'error': 'Invalid report_type parameter'})

        # Group sales data by date_added
        sales_summary = sales_data.values('date_added__date').annotate(
            sales_count=Count('id'),
            online_customer_count=Count('id', filter=Q(sales_type='online')),
            walk_in_customer_count=Count('id', filter=Q(sales_type='walk-in')),
            completed_count=Count('id', filter=Q(status='completed')),
            mpesa_count=Count('id', filter=Q(paymethod='mpesa') | Q(paymethod='mpesa_on_delivery')),
            cash_count=Count('id', filter=Q(paymethod='cash')),
            pending_count=Count('id', filter=Q(status='pending')),
            total=Sum('grand_total') or 0,
        )
        report_data={
            'sales_summary': sales_summary,
            'total_sales': sales_data.aggregate(Sum('grand_total'))['grand_total__sum'] or 0

        }

        return Response(report_data)
