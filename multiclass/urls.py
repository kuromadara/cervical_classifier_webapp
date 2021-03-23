from django.urls import path
from django.conf.urls import url
from . import views

app_name = 'multiclass'

urlpatterns = [
    path('', views.login, name=''),
    path('home', views.index, name='home'),
    path('validate', views.validate_login, name='validate'),
    path('logout', views.logout, name='logout')
]