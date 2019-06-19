from django.urls import path, include
from myserver import views

# User in url template tag: eg. {% url 'mydjango:index' %}.
app_name = 'myserver'

urlpatterns = [
    path('', views.index, name='index'),
    path('swedish/', views.DictListView.as_view(), name='dict_list'),
    path('swedish/practice', views.DictPracticeListView.as_view(), name='dict_practice'),
    path('swedish/new/', views.dict_create, name='dict_create'),
    path('swedish/<int:pk>/', views.DictDetailView.as_view(), name='dict_detail'),
    path('swedish/<int:pk>/delete/', views.remove_word, name='remove_word'),
    path('swedish/<int:pk>/remember/', views.remember_word, name='remember_word'),
    path('swedish/<int:pk>/add/', views.add_to_dict, name='add_to_dict'),
]
