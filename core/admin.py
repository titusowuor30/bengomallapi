from django.contrib import admin
from .models import *

# Register your models here.


class FrontStoreAdmin(admin.ModelAdmin):
    list_display = ('flash_sale_end_date', 'slider_text', 'slider_image',)
    list_editable = ('slider_text', 'slider_image',)
    list_display_links = ['flash_sale_end_date']


admin.site.register(FrontStore, FrontStoreAdmin)

class BlogPostInline(admin.TabularInline):
    model=Post
    extra=0

class BlogAdmin(admin.ModelAdmin):
    inlines=[BlogPostInline]
    list_display = ('title', 'date_created', 'published',)
    list_filter = ('title', 'date_created', 'published',)
    search_fields = ('title', 'date_created', 'published',)
    list_editable = ('title', 'published',)
    list_display_links = ['date_created']
admin.site.register(Post)
admin.site.register(Blog,BlogAdmin)
admin.site.register(EmailConfig)
