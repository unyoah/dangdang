from django.urls import path
from car import views

app_name = 'car'
urlpatterns = [
    path('to_car/', views.to_car, name='to_car'),
    path('add_car/', views.add_car, name='add_car'),
    path('del_car/', views.del_car, name='del_car'),
    path('set_car/', views.set_car, name='set_car'),

]
