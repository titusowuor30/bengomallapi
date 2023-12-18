from django.db import models
from product.models import Products
from human_resource.models import Customer, PickupStations
from stockinventory.models import StockInventory

class Order(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    order_id = models.CharField(max_length=50, default='36477481')
    created_at = models.DateTimeField(auto_now_add=True)
    order_amount = models.DecimalField(
        max_digits=8, decimal_places=2)
    payment_status = models.CharField(max_length=50, default='pending')
    confirm_status = models.CharField(max_length=50, default='pending')
    dispatch_status = models.CharField(max_length=50, default='pending')
    delivery_address = models.ForeignKey(PickupStations, on_delete=models.CASCADE,related_name='orders')
    delivery_from_date = models.DateTimeField(blank=True, null=True)
    delivery_to_date = models.DateTimeField(blank=True, null=True)
    delivered_status = models.CharField(max_length=100, default='pending')

    class Meta:
        ordering = ['-created_at']
        db_table = "order"
        managed = True
        verbose_name_plural = "Order"

    def __str__(self):
        return self.order_id


class Invoice(models.Model):
    customer = models.ForeignKey(
        Customer, on_delete=models.CASCADE, related_name='invoices')
    order = models.ForeignKey(
        Order, on_delete=models.CASCADE, related_name='invoices', blank=True, null=True)
    invoice_id = models.CharField(max_length=50, default='36477481')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(blank=True, null=True)
    amount = models.DecimalField(
        max_digits=8, decimal_places=2)
    status = models.CharField(max_length=50, default='pending')


    class Meta:
        ordering = ['-created_at']
        db_table = "invoices"
        managed = True
        verbose_name_plural = "Invoices"

    def __str__(self):
        return self.invoice_id


class OrderItem(models.Model):
    order = models.ForeignKey(
        Order, related_name='orderitems', on_delete=models.CASCADE)
    stock = models.ForeignKey(StockInventory,on_delete=models.CASCADE,related_name='orderitems')
    retail_price = models.DecimalField(max_digits=8, decimal_places=2)
    quantity = models.IntegerField(default=0)
    total = models.IntegerField(default=0)

    def __str__(self):
        return '%s' % self.id

    class Meta:
        db_table = "orderitems"
        managed = True
        verbose_name_plural = "Order Items"

    def get_total_retail_price(self):
        return self.retail_price * self.quantity


