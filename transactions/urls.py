from django.urls import path
from . import views

urlpatterns = [
   # path('', views.home, name='home'),  # דף הבית
    path('clients/', views.client_list, name='client_list'),
    path('clients/new/', views.client_create, name='client_create'),
    path('clients/<int:pk>/edit/', views.client_update, name='client_update'),
    path('clients/<int:pk>/delete/', views.client_delete, name='client_delete'),
    path('invoices/', views.invoice_list, name='invoice_list'),
    path('invoices/new/', views.invoice_create, name='invoice_create'),
  #  path('login/', views.login_view, name='login'),  # דף התחברות
  #  path('logout/', views.logout_view, name='logout'),  # דף התנתקות
]
