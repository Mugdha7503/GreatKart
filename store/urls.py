from django.urls import path
from . import views

urlpatterns = [
    path('',views.store, name='store'),
    path('category/<slug:category_slug>/', views.store, name='products_by_category'),
    path('category/<slug:category_slug>/<slug:product_slug>/', views.product_detail, name='product_detail'),
    path('search/',views.search, name='search'),
    
    path('', views.store_home, name='store_home'),
    path('seller_dashboard/', views.seller_dashboard, name='seller_dashboard'),
    path('buyer_home/', views.buyer_home, name='buyer_home'),
    path('add/', views.add_product, name='add_product'),
    path('seller/edit/<int:pk>/', views.edit_product, name='edit_product'),
    path('seller/delete/<int:pk>/', views.delete_product, name='delete_product'),
] 


