from django.urls import path
from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from users.views import UserViewSet
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from django.contrib.auth.views import LoginView, LogoutView


#from calculations.views import CalculationViewSet

router = DefaultRouter()
# router.register('users', UserViewSet)
# router.register('calculations', CalculationViewSet)
router.register(r'users', UserViewSet, basename='user')


urlpatterns = [
    path('home/', include('transactions.urls')),
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
    path('login/', TokenObtainPairView.as_view(), name='login'),
    path('refresh/', TokenRefreshView.as_view(), name='refresh'),
    #path('transactions/', include('transactions.urls')),
    path('api/transactions/', include('transactions.urls')),  # עדכון זה
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
 #   path('login/', LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('transactions/', include('transactions.urls')),

 
]
