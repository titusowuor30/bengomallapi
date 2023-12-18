from django.contrib import admin
from .models import *
# Register your models here.
class StockInventoryAdmin(admin.ModelAdmin):
    list_display = (
        'product','size','stock_level', 'reorder_level', 'availability',
        'is_new_arrival', 'is_favorite', 'is_flash_sale', 'is_deal_of_the_day', 'is_top_pick'
    )
    list_editable = ['stock_level', 'reorder_level', 'availability',
                     'is_new_arrival', 'is_favorite', 'is_flash_sale', 'is_deal_of_the_day', 'is_top_pick']
    list_display_links = ['product']  # Choose a field for editing links

    list_filter = ('product__title', 'product__retail_price','size__size','size__unit__unit_symbol','availability', 'is_new_arrival', 'is_favorite', 'is_flash_sale', 'is_deal_of_the_day', 'is_top_pick')
    search_fields = ('product__title', 'product__retail_price','size__size','size__unit__unit_symbol')

    fieldsets = [
        ('Product Information', {
            'fields': ['product', 'stock_level', 'reorder_level', 'size', 'color'],
        }),
        ('Additional Information', {
            'fields': ['usage', 'sku', 'serial', 'supplier', 'slider_image'],
        }),
        ('Availability and Promotions', {
            'fields': ['availability', 'is_new_arrival', 'is_favorite', 'is_flash_sale', 'is_deal_of_the_day', 'is_top_pick'],
        }),
    ]

admin.site.register(StockInventory, StockInventoryAdmin)
admin.site.register([Review])
