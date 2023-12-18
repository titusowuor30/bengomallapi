from django.contrib import admin
from .models import *
from django import forms

# Register your models here.
admin.site.register(Category)
admin.site.register(Subcategory)
admin.site.register(ProductImages)
admin.site.register([MainCategory, Favourites,ProductSize,ProductColor,Unit])

class ProductColorInline(admin.TabularInline):
    model=ProductColor
    extra=1

class ProductSizeInline(admin.TabularInline):
    model=ProductSize
    extra=1

class ProductImagesInline(admin.TabularInline):
    model=ProductImages
    extra=1

class ProductsAdmin(admin.ModelAdmin):
    inlines = [ProductImagesInline,ProductColorInline,ProductSizeInline,]
    list_display = ['title','maincategory','status', 'vendor','model',]
    list_filter = ['title', 'maincategory',
                   'maincategory__categories', 'vendor', 'status', 'model',]
    search_fields = ['title', 'maincategory__name',
                     'maincategory__categories__name', 'vendor__user__email', 'status', 'model',]
    list_editable = ['maincategory', 'vendor', 'status', 'model',]
    list_display_links=['title']

    fieldsets = (
        ('Product Information', {
            'fields': ('maincategory', 'vendor', 'model', 'title', 'description', 'retail_price', 'discount_price', 'status', 'date_added', 'weight', 'dimentions')
        }),
        )
admin.site.register(Products,ProductsAdmin)