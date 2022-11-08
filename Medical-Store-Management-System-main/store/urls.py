from django.urls import path
from store import views

app_name = 'store'
urlpatterns = [
    path('', views.index, name='store-home'),
    path('register/staff/', views.staff_register, name='staff-register'),
    path('register/bill/', views.bill_register, name='bill-register'),
    path('register/stock/', views.stock_register, name='stock-register'),
    path('register/medicine/', views.medicine_register, name='medicine-register'),
    path('register/supplier', views.supplier_register, name='supplier-register'),
    path('staff/all/', views.staff_all, name='staff-all'),
    path('staff/delete/<int:pk>/', views.staff_delete, name='staff-delete'),
    path('staff/update/<int:pk>/', views.staff_update, name='staff-update'),
    path('medicine/all/', views.medicine_all, name='medicine-all'),
    path('medicine/delete/<int:pk>/', views.medicine_delete, name='medicine-delete'),
    path('medicine/update/<int:pk>/', views.medicine_update, name='medicine-update'),
    path('supplier/all/', views.supplier_all, name='supplier-all'),
    path('supplier/delete/<int:pk>/', views.supplier_delete, name='supplier-delete'),
    path('supplier/update/<int:pk>/', views.supplier_update, name='supplier-update'),
    path('developers/', views.info, name='info'),
    path('bill/all/', views.bill_all, name='bill-all'),
    path('stock/all/', views.stock_all, name='stock-all'),
    path('stock/sort/medicine/', views.stock_med_sort, name='stock-med-sort')
]