from django.urls import path
from index import views

app_name = 'index'

urlpatterns = [
    path('index/', views.index, name='index'),
    path('book_detail/', views.book_detail, name='book_detail'),
    path('book_list/', views.book_list, name='book_list'),
]
