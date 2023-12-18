from django.db import models
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
# Create your models here.
User = get_user_model()


class Employee(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name='employee')
    national_id = models.CharField(max_length=10)
    position = models.ForeignKey(
        Group, on_delete=models.SET_NULL, blank=True, null=True)
    salary = models.PositiveIntegerField(default=1000)

    class Meta:
        db_table="employees"
        managed = True
        verbose_name_plural = "Employees"

    def __str__(self) -> str:
        return self.user.username


class Supplier(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name='supplier')
    name = models.CharField(max_length=255)
    address = models.ManyToManyField('BusinessAddress')
    delivery_regions=models.ManyToManyField("DeliveryRegions",blank=True, null=True)

    class Meta:
        db_table="suppliers"
        managed = True
        verbose_name_plural = "Suppliers"

    def __str__(self) -> str:
        return self.name


class Customer(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name='customer')
    
    class Meta:
        db_table="customers"
        managed = True
        verbose_name_plural = "Customers"

    def __str__(self) -> str:
        return self.user.username

class BusinessAddress(models.Model):
    state = models.CharField(max_length=50)
    city = models.CharField(max_length=50)
    box=models.CharField(max_length=500,default="00100-397")
    street_or_road=models.CharField(verbose_name='Street/Road',max_length=255,default='Along Kisumu-Busia Road')
    phone = models.CharField(
        max_length=15, default="07000043578", blank=True, null=True)
    other_phone = models.CharField(
        max_length=15, default="07000043578", blank=True, null=True)

    class Meta:
        db_table="business_addresses"
        managed = True
        verbose_name_plural = "Business Addresses"

    def __str__(self):
        return self.box

class AddressBook(models.Model):
    customer=models.ForeignKey(Customer,on_delete=models.CASCADE,related_name='addresses',blank=True,null=True)
    address_label=models.CharField(max_length=255,default='my address 1')
    phone = models.CharField(
        max_length=15, default="07000043578", blank=True, null=True)
    other_phone = models.CharField(
        max_length=15, default="07000043578", blank=True, null=True)
    region=models.ForeignKey("DeliveryRegions",on_delete=models.CASCADE,related_name='address')
    city=models.ForeignKey("PickupStations",on_delete=models.CASCADE,related_name='address')
    postal_code=models.CharField(max_length=100,default="57-40100", blank=True, null=True)
    default_address = models.BooleanField(default=False,verbose_name="Default Address")

    class Meta:
        db_table="address_book"
        managed = True
        verbose_name_plural = "AddressBook"

    def __str__(self):
        return self.customer.user.first_name+" "+self.customer.user.last_name


class DeliveryRegions(models.Model):
    region = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    door_step_delivery = models.BooleanField(default=False)
    door_step_delivery_charge = models.PositiveBigIntegerField(
        default=300, blank=True, null=True)

    def __str__(self):
        return self.region

    class Meta:
        db_table="delivery_regions"
        managed = True
        verbose_name_plural = "Delivery Regions"


class PickupStations(models.Model):
    region=models.ForeignKey(DeliveryRegions,on_delete=models.CASCADE,related_name='pickupstations',blank=True, null=True)
    pickup_location = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    open_hours = models.CharField(
        max_length=255, default="Mon-Fri 0800hrs - 1700hrs;Sat 0800hrs - 1300hrs")
    payment_options = models.CharField(
        max_length=500, default="MPESA On Delivery, Cards")
    google_pin = models.URLField(
        max_length=1500, default="https://goo.gl/maps/p2QAwb7jbmxuJcb36")
    helpline = models.CharField(
        max_length=20, default="076353535353")
    shipping_charge = models.PositiveBigIntegerField(default=85)

    def __str__(self):
        return self.pickup_location

    class Meta:
        managed = True
        db_table="pickup_stattions"
        verbose_name_plural = "Pickup Stations"
