from datetime import datetime
from unicodedata import category
from django.db import models
from django.utils import timezone
from django.contrib.auth import get_user_model
from vendor.models import Vendor

User = get_user_model()
# Create your models here.

class Unit(models.Model):
    unit_title = models.CharField(max_length=50)
    unit_symbol = models.CharField(max_length=50)

    def __str__(self):
        return self.unit_symbol

    class Meta:
        db_table = "units"
        managed = True
        verbose_name_plural = "Units"

class MainCategory(models.Model):
    categories = models.ManyToManyField(
        "Category", null=True, blank=True)
    name = models.CharField(max_length=255)
    display_image = models.ImageField(
        upload_to='maincategory/display', null=True, blank=True)
    status = models.IntegerField(default=1)

    def __str__(self):
        return self.name

    class Meta:
        db_table = "main_categories"
        managed = True
        verbose_name_plural = "Main Categories"


class Category(models.Model):
    Subcategories = models.ManyToManyField(
        "Subcategory", null=True, blank=True)
    name = models.CharField(max_length=255)
    display_image = models.ImageField(
        upload_to='category/display', null=True, blank=True)
    status = models.IntegerField(default=1)

    def __str__(self):
        return self.name

    class Meta:
        db_table = "categories"
        managed = True
        verbose_name_plural = "Categories"


class Subcategory(models.Model):
    name = models.CharField(max_length=255)
    display_image = models.ImageField(
        upload_to='category/subcategory/display', null=True, blank=True)
    status = models.IntegerField(default=1)

    def __str__(self):
        return self.name

    class Meta:
        db_table = "subcategories"
        managed = True
        verbose_name_plural = "Sub Categories"


class ProductImages(models.Model):
    product=models.ForeignKey("Products",on_delete=models.SET_NULL,related_name='images',null=True,blank=True)
    image = models.FileField(upload_to="products/%Y%m%d/")

    def __str__(self):
        return self.image.url if self.image else None

    class Meta:
        db_table = "productimages"
        managed = True
        verbose_name_plural = "Images"


class Products(models.Model):
    maincategory = models.ForeignKey(
        MainCategory, on_delete=models.CASCADE, null=True, blank=True,related_name='products')
    vendor = models.ForeignKey(
        Vendor, on_delete=models.CASCADE, related_name="products", null=True, blank=True)
    model = models.CharField(max_length=255, blank=True, null=True)
    title = models.TextField(max_length=500, default="Hp x2 1033")
    description = models.TextField()
    unit_price = models.FloatField(default=0,help_text='Enter general price or leave it as 0.0 and set unit price in variations')
    retail_price = models.FloatField(default=0,help_text='Enter general price or leave it as 0.0 and set unit price in variations')
    discount_price = models.FloatField(default=0, null=True, blank=True,help_text='Enter general discount price or leave it as 0.0 and set unit price in variations')
    status = models.IntegerField(default=1)
    date_added = models.DateTimeField(default=timezone.now)
    date_updated = models.DateTimeField(auto_now=True)
    weight = models.CharField(max_length=255, blank=True, null=True)
    dimentions = models.CharField(
        max_length=50, default="1x2x3", blank=True, null=True)


    def __str__(self):
        return self.title

    class Meta:
        db_table = 'products'
        managed = True
        verbose_name = 'Products'
        verbose_name_plural = 'Products'

    def product_total(self):
        return self

class ProductSize(models.Model):
    product = models.ForeignKey(Products, on_delete=models.CASCADE,related_name='sizes')
    size = models.CharField(max_length=10,default="0")
    unit=models.ForeignKey(Unit,on_delete=models.SET_NULL,related_name='sizes',null=True)
    unit_price=models.FloatField(max_length=100,default=0)
    retail_price=models.FloatField(max_length=100,default=0)
    unit_discount_price=models.FloatField(max_length=100,default=0,null=True,blank=True)

    class Meta:
        verbose_name='Size Variation'
        verbose_name_plural='Size Variation'

    def __str__(self):
        return str(self.size) + " " + str(self.unit.unit_title)

class ProductColor(models.Model):
    product = models.ForeignKey(Products, on_delete=models.CASCADE,related_name='colors',null=True,blank=True)
    color = models.CharField(max_length=20)

    class Meta:
        verbose_name='Color Variation'
        verbose_name_plural='Color Variation'

    def __str__(self):
        return self.color


class Favourites(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(
        Products, on_delete=models.CASCADE, related_name='favourites')
    size=models.ForeignKey(ProductSize, on_delete=models.CASCADE, related_name='favourites',blank=True,null=True)
    color=models.ForeignKey(ProductColor, on_delete=models.CASCADE, related_name='favourites',blank=True,null=True)
    is_favorite=models.BooleanField(default=False)

    def __str__(self):
        return self.product.title

    class Meta:
        db_table = 'savedproducts'
        managed = True
        verbose_name = 'Favourites'
        verbose_name_plural = 'Favourites'
