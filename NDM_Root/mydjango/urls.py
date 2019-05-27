from django.urls import path
from mydjango import views

# User in url template tag: eg. {% url 'mydjango:index' %}.
app_name = 'mydjango'

urlpatterns = [
    path('', views.index, name='index'),
    path('postgres/', views.postgres, name='postgres'),
    path('user/', views.user, name='user'),
    path('background/', views.background, name='background'),
]
