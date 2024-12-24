from django.urls import path
from rest_framework_nested import routers
from . import views

router = routers.DefaultRouter()
router.register('products', views.ProductViewSet)

product_router = routers.NestedDefaultRouter(router,'products',lookup='product')


urlpatterns = router.urls + product_router.urls