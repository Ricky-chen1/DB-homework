# user/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('register', views.register_view, name='register'),
    path('login', views.login_view, name='login'),
    path('name/<int:user_id>',views.get_user_name,name='get_user_name')
]