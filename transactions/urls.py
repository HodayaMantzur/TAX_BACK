from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),  # דף הבית
    path('login/', views.user_login, name='login'),  # התחברות משתמש רגיל
    path('admin_dashboard/', views.admin_dashboard, name='admin_dashboard'),  # דף ניהול אדמין
    path('client_dashboard/', views.client_dashboard, name='client_dashboard'),  # דף ניהול יוזר
    path('clients/', views.client_list_create, name='client_list_create'),  # רשימת לקוחות או יצירת לקוח
    path('clients/<int:pk>/', views.client_update_delete, name='client_update_delete'),  # עדכון או מחיקת לקוח
    path('invoices/', views.invoice_list, name='invoice_list'),  # רשימת חשבוניות
    path('invoices/create/', views.invoice_create, name='invoice_create'),  # יצירת חשבונית חדשה
    path('register/', views.register_user, name='register_user'),
    path('me/', views.get_user_details, name='get_user_details'),

]

# from django.urls import path
# from . import views

# urlpatterns = [
#     path('', views.home, name='home'),  # דף הבית עם כפתור לוגין וכפתור אדמין
#     path('client_login/', views.client_login, name='client_login'),  # כניסת יוזר
#     path('admin_login/', views.admin_login, name='admin_login'),  # כניסת אדמין
#     path('client_list/', views.client_list, name='client_list'),  # רשימת לקוחות
#     path('client_create/', views.client_create, name='client_create'),  # יצירת לקוח
#    # path('client_update/<int:pk>/', views.client_update, name='client_update'),  # עדכון לקוח
#    # path('client_delete/<int:pk>/', views.client_delete, name='client_delete'),  # מחיקת לקוח
#    # path('invoice_list/', views.invoice_list, name='invoice_list'),  # רשימת הפקות הכנסות
#     path('invoice_create/', views.invoice_create, name='invoice_create'),  # יצירת הפקת הכנסה
#     path('client_dashboard/', views.client_dashboard, name='client_dashboard'),  # רק לקוח של אותו יוזר

# ]





# from django.urls import include, path
# from . import views
# from users.views import UserViewSet  # ייבוא מהיוזרס
# from rest_framework.routers import DefaultRouter
# from users.views import UserViewSet
# from rest_framework_simplejwt.views import TokenObtainPairView
# from django.contrib.auth.views import LogoutView

# router = DefaultRouter()
# router.register(r'users', UserViewSet, basename='user')

# urlpatterns = [
#     path('home/', views.home, name='home'),  # דף הבית
#     path('clients/', views.client_list, name='client_list'),
#     path('clients/new/', views.client_create, name='client_create'),
#     path('clients/<int:pk>/edit/', views.client_update, name='client_update'),
#     path('clients/<int:pk>/delete/', views.client_delete, name='client_delete'),
#     path('invoices/', views.invoice_list, name='invoice_list'),
#     path('invoices/new/', views.invoice_create, name='invoice_create'),

#     # נתיבי הלוגין ללקוח ולמנהל
#     path('login-client/', views.client_login, name='login_client'),  # לוגין ללקוח
#     path('login-admin/', views.admin_login, name='login_admin'),  # לוגין למנהל

#     # נתיב ה-API של העסקאות
#     path('api/transactions/clients/', views.client_list, name='client_list'),
#     path('api/transactions/clients/new/', views.client_create, name='client_create'),
#     path('api/transactions/clients/<int:pk>/edit/', views.client_update, name='client_update'),
#     path('api/C/clients/<int:pk>/delete/', views.client_delete, name='client_delete'),

#     # אם יש נתיבים נוספים (כמו api)
#     #path('api/', include('transactions.urls')),
# ]


