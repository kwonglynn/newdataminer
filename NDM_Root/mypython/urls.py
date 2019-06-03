from django.urls import path
from mypython import views
from .views import ModuleListView, ModuleDetailView

# User in url template tag: eg. {% url 'mydjango:index' %}.
app_name = 'mypython'

urlpatterns = [
    path('', views.index, name='index'),
    path("conda/", views.conda, name='conda'),
    path('ddns/', views.ddns, name='ddns'),
    path('module_form/', views.module_form, name='module_form'),
    path('modules/', ModuleListView.as_view(), name='modules'),
    path('modules/<slug:title>', ModuleDetailView.as_view(), name='module_detail'),
]
