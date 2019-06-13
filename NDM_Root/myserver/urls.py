from django.urls import path, include
from myserver import views

# User in url template tag: eg. {% url 'mydjango:index' %}.
app_name = 'myserver'

urlpatterns = [
    path('', views.index, name='index'),
    path('swedish/new/', views.dict_create, name='dict_create'),
    # path('swedish/new/', views.dictCreateView.as_view(), name='dict_create'),
    path('swedish/<int:pk>/', views.DictDetailView.as_view(), name='dict_detail'),
    path('swedish/<int:pk>/delete/', views.DictDeleteView.as_view(), name='dict_delete'),
    path('swedish/<int:pk>/add/', views.publish, name='publish'),
    path('swedish/list/', views.DictListView.as_view(), name='dict_list'),
]
