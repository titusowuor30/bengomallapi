from django.db import models

# Create your models here.


class Transactions(models.Model):
    orderid = models.CharField(max_length=255, default='644748')
    checkoutid = models.CharField(max_length=255)
    timestamp = models.CharField(max_length=255)
    secret = models.CharField(max_length=1500)
    status = models.CharField(max_length=100, default='success')

    def __str__(self):
        return self.timestamp

    class Meta:
        db_table = "transactions"
        managed = True
        verbose_name_plural = "Transactions"
