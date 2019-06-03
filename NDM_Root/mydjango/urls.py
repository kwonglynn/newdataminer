from django.urls import path
from mydjango import views

# User in url template tag: eg. {% url 'mydjango:index' %}.
app_name = 'mydjango'

urlpatterns = [
    path('', views.index, name='index'),
    path('postgres/', views.postgres, name='postgres'),
    path('mysql/', views.mysql, name='mysql'),
    path('user/', views.user, name='user'),
    path('background/', views.background, name='background'),
    path('channels/', views.channels, name='channels'),
    path('email_server/', views.email_server, name='email_server'),
    path('slug/', views.slug, name='slug'),
]
