from django.urls import path
from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from users.views import UserViewSet
from calculations.views import CalculationViewSet

router = DefaultRouter()
router.register('users', UserViewSet)
router.register('calculations', CalculationViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
      
]
