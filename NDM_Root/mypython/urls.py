from django.urls import path
from mypython import views

urlpatterns = [
    path('', views.index, name='index')
]
