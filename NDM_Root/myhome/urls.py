from django.urls import path, include
from myhome import views
from myhome.views import Register

app_name = 'myhome'

urlpatterns = [
    path('', views.index, name='index'),
    path('register-success/', views.register_success, name="register-success"),
    path('register/', Register.as_view(), name='register'),
    path('contact/', views.contact, name='contact'),
    path('search/', include('haystack.urls')),
]
