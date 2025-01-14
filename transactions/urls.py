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

