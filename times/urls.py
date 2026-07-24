from django.urls import path
from . import views

urlpatterns = [
    path('', views.time_list, name='time-list'),
    path('novo-time/', views.time_create, name='time-create')
]