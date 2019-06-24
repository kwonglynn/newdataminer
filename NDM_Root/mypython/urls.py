from django.urls import path, include
from mypython import views

# User in url template tag: eg. {% url 'mydjango:index' %}.
app_name = 'mypython'

urlpatterns = [
    path('', views.index, name='index'),
    path("conda/", views.conda, name='conda'),
    path("plotly/", views.plotly, name="plotly"),
    path('ddns/', views.ddns, name='ddns'),
    path('modules/', views.ModuleListView.as_view(), name='module_list'),
    path('modules/new/', views.module_create, name='module_create'),
    # path('modules/new/', views.ModuleCreateView.as_view(), name='module_create'),
    path('modules/<int:pk>/', views.ModuleDetailView.as_view(), name='module_detail'),
    path('modules/<int:pk>/update/', views.ModuleUpdateView.as_view(), name="module_update"),
    path('modules/<int:pk>/delete/', views.ModuleDeleteView.as_view(), name='module_delete'),
    path('modules/<int:pk>/publish/', views.module_publish, name='module_publish'),
    path('modules/drafts/', views.DraftListView.as_view(), name='module_draft_list'),
    # path('modules/drafts/', views.DraftListView.as_view(), name="module_draft_list"),
]
