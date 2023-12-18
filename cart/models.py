from django.db import models
from product.models import Products
from authmanagement.models import MyUser
from stockinventory.models import StockInventory
# Create your models here.


class Cart(models.Model):
    user = models.ForeignKey(MyUser, on_delete=models.CASCADE,related_name='cart')
    stock=models.ForeignKey(StockInventory,on_delete=models.CASCADE,related_name='cart')
    quantity = models.PositiveIntegerField(default=0)
    tax=models.FloatField(default=0)
    retail_price=models.FloatField(default=0)
    item_subtotal=models.FloatField(default=0)
    item_total=models.FloatField(default=0)


    def __str__(self) -> str:
        return "{} [{}]".format(self.stock.product.title, self.quantity)

    class Meta:
        db_table = 'cart'
        managed = True
        verbose_name = 'Cart'
        verbose_name_plural = 'cart'
