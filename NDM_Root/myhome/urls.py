from django.urls import path
from myhome import views

app_name = 'myhome'

urlpatterns = [
    path('', views.index, name='index'),
]
