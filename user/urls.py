from django.urls import path
from user import views

app_name = 'user'

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.login, name='login'),
    path('reg/', views.reg, name='reg'),
    path('log/', views.log, name='log'),
    path('log_out/', views.log_out, name='log_out'),
    path('reg_ok/', views.reg_ok, name='reg_ok'),
    path('captcha/', views.captcha, name='captcha'),

]
