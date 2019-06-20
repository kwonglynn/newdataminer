from django.urls import path, include
from myserver import views

# User in url template tag: eg. {% url 'mydjango:index' %}.
app_name = 'myserver'

urlpatterns = [
    path('', views.index, name='index'),
    path('swedish/table/', views.DictListView.as_view(), name='dict_list_table'),
    path('swedish/card/', views.DictListView.as_view(), name='dict_list_card'),
    path('swedish/table/today/', views.DictListView.as_view(), name='dict_list_table_today'),
    path('swedish/card/today/', views.DictListView.as_view(), name='dict_list_card_today'),
    path('swedish/practice/', views.DictPracticeListView.as_view(), name='dict_practice'),
    path('swedish/practice/today/', views.DictPracticeListView.as_view(), name='dict_practice_today'),
    path('swedish/new/', views.dict_create, name='dict_create'),
    path('swedish/<int:pk>/table', views.DictDetailView.as_view(), name='dict_detail_table'),
    path('swedish/<int:pk>/card', views.DictDetailView.as_view(), name='dict_detail_card'),
    path('swedish/<int:pk>/delete/', views.remove_word, name='remove_word'),
    path('swedish/<int:pk>/remember/', views.remember_word, name='remember_word'),
    path('swedish/<int:pk>/add/', views.add_to_dict, name='add_to_dict'),
]
