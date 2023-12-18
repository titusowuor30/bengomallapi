
from django.urls import path, include
from rest_framework import routers
from .views import *
from .utils import *

router = routers.DefaultRouter()
router.register('maincategories', MainCategoryViewSet)
router.register('categories', CategoryViewSet)
router.register('subcategories', SubCategoryViewSet)
router.register('productcolors', ProductColorViewSet)
router.register('productsizes', ProductSizeViewSet)
router.register('products', ProductViewSet)
router.register('favourites', ReviewsViewSet)
router.register('reviews', ReviewsViewSet)


urlpatterns = [
    path('', include(router.urls)),
    path('add-product/<int:id>/', addProduct),
    path('import_products/', LoadExcelProducts.as_view()),
    path('product/<int:pk>/', ProductDetail.as_view()),
    path('favorites/<int:pk>/', MarkAsFavorite.as_view(), name='mark-favorite'),
    path('favorites/', MarkAsFavorite.as_view(), name='mark-favorite'),
]
