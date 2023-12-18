from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import *
from django.shortcuts import render
from datetime import date, datetime
from .models import *
from rest_framework.views import APIView
from rest_framework.response import Response
from pos.models import *
from django.http import Http404
from rest_framework.views import APIView
from rest_framework import viewsets
from rest_framework.decorators import api_view, permission_classes
from rest_framework import permissions, authentication
from .serializers import *
from human_resource.models import Supplier
from stockinventory.models import StockInventory
from stockinventory.serializers import *
import json
from rest_framework.pagination import LimitOffsetPagination

# add product
@api_view(['POST', 'PUT'])
@permission_classes([permissions.IsAuthenticated,])
def addProduct(request, id=0):
    #try:
        sku = request.POST.get('sku')
        model = request.POST.get('model')
        title = request.POST.get('title')
        description = request.POST.get('description')
        retail_price = request.POST.get('retail_price')
        discount_price = request.POST.get('discount_price')
        status = request.POST.get('status')
        weight = request.POST.get('weight')
        dimentions = request.POST.get('dimensions')
        colors = json.loads(request.POST.get('colors'))
        sizes = json.loads(request.POST.get('sizes'))
        availability = request.POST.get('availability')
        maincategory = MainCategory.objects.get(
            id=request.POST.get('maincategories'))
        category = Category.objects.filter(
            name__in=json.loads(request.POST.get('categories')))
        subcategories = Subcategory.objects.filter(
            name__in=json.loads(request.POST.get('subcategories')))
        vendor = Vendor.objects.filter(user__id=int(request.POST.get('vendor'))).first()
        productimages = request.FILES.getlist('images')
        stock_level = request.POST.get('stock_level')
        reorder_level = request.POST.get('reorder_level')
        supplier = Supplier.objects.filter(id=int(request.POST.get('supplier'))).first()
        if id == 0:
            # add product
            product = Products(
                model=model,
                title=title,
                description=description,
                retail_price=retail_price,
                discount_price=discount_price,
                status=status,
                weight=weight,
                dimentions=dimentions,
            )
            product.vendor = vendor
            product.save()
            subcats = []
            maincat = None
            if maincategory:
                maincat = MainCategory.objects.get(id=maincategory.pk)
                product.maincategory = maincat
            if category:
                for cat in category:
                    maincat.categories.add(cat)
                    if subcategories:
                        for sbc in subcategories:
                            cat.Subcategories.add(sbc)
            if len(sizes)==0 and len(colors)==0:
               stock,created=StockInventory.objects.get_or_create(product=product,availability=availability,
                                                                 sku=sku,stock_level=stock_level,
                                                                  reorder_level=reorder_level,size=None,color=None,
                                                                  supplier=supplier)
            # add variations
            if len(sizes)>0:
                print(sizes)
                for s in sizes:
                    print(s)
                    item_unit,created=Unit.objects.get_or_create(unit_title=s['unit'],unit_symbol=s['unit'])
                    sz, created = ProductSize.objects.get_or_create(product=product,size=s['size'],
                                                                    retail_price=s['retail_price'],
                                                                    unit_discount_price=s['unit_dicount_retail_price'])
                    sz.unit=item_unit
                    sz.save()
                    stock,created=StockInventory.objects.get_or_create(product=product,availability=availability,
                                                                       usage=s['usage'],sku=s['sku'],serial=s['serial'],
                                                                        size=None,color=None,supplier=supplier)
                    stock.size=sz
                    stock.stock_level=s['stock_level']
                    stock.reorder_level=s['reorder_level']
                    stock.save()
            if len(colors)>0:
                for cl in colors:
                    color, created = ProductColor.objects.get_or_create(product=product,color=cl['color'])
                    stock,created=StockInventory.objects.get_or_create(product=product,availability=availability,usage=cl['usage'],sku=cl['sku'],serial=cl['serial'],size=None,color=None,supplier=supplier)
                    stock.color=color
                    stock.stock_level=cl['stock_level']
                    stock.reorder_level=cl['reorder_level']
                    stock.save()
            if productimages:
                for img in productimages:
                    _,created=ProductImages.objects.get_or_create(product=product,image=img)
            product.save()
        else:
            # upate product
            product_instance = Products.objects.get(id=id)
            product_instance.title = title
            product_instance.description = description
            product_instance.weight = weight
            product_instance.dimentions = dimentions
            product_instance.model = model
            product_instance.status = 1
            product_instance.retail_price = retail_price
            product_instance.discount_price = discount_price
            product_instance.vendor = vendor
            product_instance.maincategory = maincategory
            for cat in category:
                maincategory.categories.set(cat)
                subcats = Category.objects.filter(
                    name__in=subcategories)
                for sbc in subcats:
                    product_instance.maincategory.categories.set(sbc)
                    cat.Subcategories.set(sbc)
             # update inventory
            stockinventory = StockInventory.objects.filter(product=product_instance)
            for stock in stockinventory:
                stock.stock_level = stock_level
                stock.reorder_level = reorder_level
                stock.supplier = supplier
                # update variations
                if len(colors) > 0:
                    for cl in colors:
                        color = ProductColor.objects.filter(product=product_instance)
                        for c in color:
                            c.color=cl['color']
                            c.save()
                            stock.color=c
                if len(sizes)>0:
                    for s in sizes:
                        sz= ProductSize.objects.filter(product=product_instance)
                        for size in sz:
                            size.size=s['size']
                            size.retail_price=s['retail_price']
                            size.unit_discount_price=s['unit_discount_price']
                            size.save()
                            stock.size=size
                #update stock
                stock.save()
            if productimages:
                for img in productimages:
                    p, updated = ProductImages.objects.update_or_create(
                        product=product,
                        image=img)
            product_instance.save()
        return Response({'msg': 'Your work has been  saved!', 'status': 'success!', 'icon': 'success'})
    # except Exception as e:
    #     return Response({'msg': str(e), 'status': 'Failed!', 'icon': 'error'})

# Create your views here.


class MainCategoryViewSet(viewsets.ModelViewSet):
    queryset = MainCategory.objects.all()
    serializer_class = MainCategoriesSerializer
    authentication_classes = []
    permission_classes = [permissions.IsAuthenticatedOrReadOnly,]
    pagination_class = LimitOffsetPagination  # Enable Limit and Offset Pagination



class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategoriesSerializer
    authentication_classes = []
    permission_classes = [permissions.IsAuthenticatedOrReadOnly,]
    pagination_class = LimitOffsetPagination  # Enable Limit and Offset Pagination


class SubCategoryViewSet(viewsets.ModelViewSet):
    queryset = Subcategory.objects.all()
    serializer_class = SubCategoriesSerializer
    authentication_classes = []
    permission_classes = [permissions.IsAuthenticatedOrReadOnly,]
    pagination_class = LimitOffsetPagination  # Enable Limit and Offset Pagination


class ProductColorViewSet(viewsets.ModelViewSet):
    queryset = ProductColor.objects.all()
    serializer_class = productColorSerializer
    permission_classes = [permissions.AllowAny,]
    pagination_class = LimitOffsetPagination  # Enable Limit and Offset Pagination

class ProductSizeViewSet(viewsets.ModelViewSet):
    queryset = ProductSize.objects.all()
    serializer_class = productSizeSerializer
    authentication_classes = []
    permission_classes = [permissions.IsAuthenticatedOrReadOnly,]
    pagination_class = LimitOffsetPagination  # Enable Limit and Offset Pagination