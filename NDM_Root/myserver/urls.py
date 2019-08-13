from django.urls import path, include
from myserver import views
import string

# User in url template tag: eg. {% url 'mydjango:index' %}.
app_name = 'myserver'

urlpatterns = [
    path('', views.index, name='index'),
    path('swedish/table/add/', views.DictCreateView.as_view(), name='dict_table_add'),
    path('swedish/card/add/', views.DictCreateView.as_view(), name='dict_card_add'),
    path('swedish/<int:pk>/table/create/', views.dict_update_create, name="dict_table_update_create"),
    path('swedish/<int:pk>/card/create/', views.dict_update_create, name="dict_card_update_create"),
    path('swedish/table/exist/', views.dict_exist, name="dict_table_exist"),
    path('swedish/card/exist/', views.dict_exist, name="dict_card_exist"),
    path('swedish/<int:pk>/table/update/', views.DictUpdateView.as_view(), name="dict_table_update"),
    path('swedish/<int:pk>/card/update/', views.DictUpdateView.as_view(), name="dict_card_update"),
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

# Generate a list of A-Z plus Ä, Å, and Ö.
letters = list(string.ascii_uppercase + 'ÄÅÖ')
for letter in letters:
    urlpatterns.append(path('swedish/table/%s' % letter, views.DictListView.as_view(), name='dict_list_table_%s' % letter))
    urlpatterns.append(path('swedish/card/%s' % letter, views.DictListView.as_view(), name='dict_list_card_%s' % letter))
