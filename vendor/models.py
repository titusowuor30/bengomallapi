from django.db import models
from django.contrib.auth import get_user_model
from human_resource.models import *
#from order.models import *
# Create your models here.
User = get_user_model()


class Vendor(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='vendor')
    name = models.CharField(max_length=255, default="TDBSoft")
    address = models.ManyToManyField(BusinessAddress)
    delivery_addresses = models.ManyToManyField(
        DeliveryRegions, blank=True, null=True, related_name='vendors')
    employees = models.ManyToManyField(Employee, blank=True, null=True,related_name='vendors')
    suppliers = models.ManyToManyField(Supplier, blank=True, null=True,related_name='vendors')
    customers = models.ManyToManyField(Customer, blank=True, null=True,related_name='vendors')

    def __str__(self):
        return self.user.username

    class Meta:
        db_table = "vendors"
        managed = True
        verbose_name_plural = "Vendors"


class Review(models.Model):
    vendor = models.ForeignKey(
        "Vendor", on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="reviews")
    text = models.TextField()
    rating = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.rating

    class Meta:
        db_table = "vendor_ratiings"
        managed = True
        verbose_name_plural = "Vendor Ratings"
