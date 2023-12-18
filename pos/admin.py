from django.contrib import admin
from .models import *

class SalesItemsInline(admin.TabularInline):
    model = salesItems

class SalesAdmin(admin.ModelAdmin):
    list_display = ('code', 'sub_total', 'grand_total', 'status', 'paymethod',
                    'sales_type', 'attendant', 'date_added', 'date_updated')
    list_filter = ('status', 'paymethod', 'sales_type', 'attendant')
    search_fields = ('code', 'status', 'paymethod', 'sales_type', 'attendant__username')
    list_editable=['sub_total', 'grand_total', 'status', 'paymethod', 'sales_type', 'attendant',]
    list_display_links=['code']
    inlines = [SalesItemsInline]

class SalesItemsAdmin(admin.ModelAdmin):
    list_display = ('sale', 'stock', 'retail_price', 'qty', 'total', 'date_added', 'date_updated')
    list_filter = ('sale', 'stock')
    search_fields = ('sale__code', 'stock__product__title')
    list_editable=['stock', 'retail_price', 'qty', 'total',]
    list_display_links=['sale']

admin.site.register(Sales, SalesAdmin)
admin.site.register(salesItems, SalesItemsAdmin)

class TransactionAdmin(admin.ModelAdmin):
    list_display = ('transactionRef', 'clientName',
                    'clientId', 'transactionType','amount', )
    list_editable = ['clientName', 'clientId', 'transactionType','amount',]
    list_display_links = ['transactionRef']  # Choose a field for editing links
    list_filter = ('clientName', 'clientId', 'transactionType',
                   'transactionRef', 'amount', )
    search_fields= ('clientName', 'clientId', 'transactionType', 'transactionRef','amount', )

admin.site.register(Transaction,TransactionAdmin)

