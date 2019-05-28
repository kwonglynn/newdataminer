from django.urls import path
from mypython import views

# User in url template tag: eg. {% url 'mydjango:index' %}.
app_name = 'mypython'

urlpatterns = [
    path('', views.index, name='index'),
    path('remote/', views.remote, name='remote'),
]
