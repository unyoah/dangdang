from django.urls import path
from order import views

app_name = 'order'
urlpatterns = [
    path('to_order/', views.to_order, name='to_order'),
    path('to_order_ok/', views.to_order_ok, name='to_order_ok'),
    path('order/', views.order, name='order'),
    path('select_addr/', views.select_addr, name='select_addr'),


]
