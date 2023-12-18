from django.db import models
from django.utils import timezone
from product.models import *
from human_resource.models import *
from stockinventory.models import StockInventory

class Sales(models.Model):
    attendant = models.ForeignKey(
        Employee, on_delete=models.DO_NOTHING, related_name="sales", blank=True, null=True)
    code = models.CharField(max_length=100, blank=True, null=True)
    sub_total = models.FloatField(default=0)
    grand_total = models.FloatField(default=0)
    tax_amount = models.FloatField(default=0)
    tax = models.FloatField(default=0)
    tendered_amount = models.FloatField(default=0)
    amount_change = models.FloatField(default=0)
    date_added = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)
    status = models.CharField(
        max_length=20, default="pending", blank=True, null=True)
    paymethod = models.CharField(max_length=20,choices=(("cash","Cash"),("mpesa","Mpesa"),("mpesa_on_delivery","Mpesa on Delivery")), default="cash", blank=True, null=True)
    sales_type = models.CharField(max_length=20,choices=(("walk-in","walk-in customer"),("online","online customer")),default="walk-in customer")

    def __str__(self):
        return self.code

    class Meta:
        db_table = 'sales'
        managed = True
        verbose_name = 'Sales'
        verbose_name_plural = 'Sales'


class salesItems(models.Model):
    sale = models.ForeignKey(
        Sales, on_delete=models.CASCADE, related_name='salesitems')
    stock = models.ForeignKey(StockInventory,on_delete=models.CASCADE,related_name='salesitems')
    retail_price = models.FloatField(default=0)
    qty = models.FloatField(default=0)
    total = models.FloatField(default=0)
    date_added = models.DateTimeField(default=timezone.now)
    date_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.sale.code+"-"+self.stock.product.title

    class Meta:
        db_table = 'salesitems'
        managed = True
        verbose_name = 'Sales Items'
        verbose_name_plural = 'Sales Items'

class Transaction(models.Model):
    clientName = models.CharField(max_length=255)
    clientId = models.CharField(max_length=255)
    transactionType = models.CharField(max_length=20,choices=(("deposit","deposit"),("withdrawal","withdrawal")),default="withdrawal")
    transactionRef = models.CharField(max_length=255)
    date = models.DateField()
    amount = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.transactionRef

    class Meta:
        db_table = 'mpesa_transactions'
        managed = True
        verbose_name = 'Mpesa Transactions'
        verbose_name_plural = 'Mpesa Transactions'