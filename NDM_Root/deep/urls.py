from django.urls import path, include
from deep import views

# User in url template tag: eg. {% url 'mydjango:index' %}.
app_name = 'deep'

urlpatterns = [
    path('methods/new/', views.deep_create, name='deep_create'),
    # path('methods/new/', views.deepCreateView.as_view(), name='deep_create'),
    path('methods/<int:pk>/', views.DeepDetailView.as_view(), name='deep_detail'),
    path('methods/<int:pk>/update/', views.DeepUpdateView.as_view(), name="deep_update"),
    path('methods/<int:pk>/delete/', views.DeepDeleteView.as_view(), name='deep_delete'),
    path('methods/<int:pk>/publish/', views.publish, name='publish'),
    path('methods/drafts/', views.DraftListView.as_view(), name='deep_draft_list'),
    path('', views.DeepListView.as_view(), name='deep_list'),    
]
