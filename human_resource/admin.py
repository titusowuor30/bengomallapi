from django.contrib import admin
from .models import *
# Register your models here.
admin.site.register([Employee, Supplier,BusinessAddress,AddressBook])

class PickupStationsInline(admin.StackedInline):
    model=PickupStations
    extra=1

class AddressBookInline(admin.StackedInline):
    model=AddressBook
    extra=1

@admin.register(DeliveryRegions)
class DeliveryRegionsAdmin(admin.ModelAdmin):
    inlines=[PickupStationsInline,]
    list_display=['region','city','door_step_delivery','door_step_delivery_charge']
    search_fields=['region','city','door_step_delivery','door_step_delivery_charge']
    list_filter=['region','city','door_step_delivery','door_step_delivery_charge']

@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    inlines=[AddressBookInline,]
    list_display=['user',]
