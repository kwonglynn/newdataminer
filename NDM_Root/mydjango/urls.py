from django.urls import path
from mydjango import views

# User in url template tag: eg. {% url 'mydjango:index' %}.
app_name = 'mydjango'

urlpatterns = [
    path('', views.index, name='index'),
    path('model', views.model, name='model'),
    path('postgres/', views.postgres, name='postgres'),
    path('mysql/', views.mysql, name='mysql'),
    path('user/', views.user, name='user'),
    path('background/', views.background, name='background'),
    path('channels/', views.channels, name='channels'),
    path('email_server/', views.email_server, name='email_server'),
    path('slug/', views.slug, name='slug'),
    path('use_js/', views.use_js, name='use_js'),
    path('use_Q/', views.use_Q, name='use_Q'),
    path('use_haystack/', views.use_haystack, name='use_haystack'),
    path('use_GSE/', views.use_GSE, name='use_GSE'),
]
