from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from foods.views import FoodViewSet
from users.views import register, login
from orders.views import add_to_cart, place_order
from django.conf.urls.static import static
from django.conf import settings

router = DefaultRouter()
router.register(r'foods', FoodViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/register/', register),
    path('api/login/', login),
    path('api/cart/add/', add_to_cart),
    path('api/order/place/', place_order),
    path('api/', include(router.urls)),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
