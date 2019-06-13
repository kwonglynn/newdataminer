from django.urls import path, include
from machine import views

# User in url template tag: eg. {% url 'mydjango:index' %}.
app_name = 'machine'

urlpatterns = [
    path('methods/new/', views.machine_create, name='machine_create'),
    # path('methods/new/', views.machineCreateView.as_view(), name='machine_create'),
    path('methods/<int:pk>/', views.MachineDetailView.as_view(), name='machine_detail'),
    path('methods/<int:pk>/update/', views.MachineUpdateView.as_view(), name="machine_update"),
    path('methods/<int:pk>/delete/', views.MachineDeleteView.as_view(), name='machine_delete'),
    path('methods/<int:pk>/publish/', views.publish, name='publish'),
    path('methods/drafts/', views.DraftListView.as_view(), name='machine_draft_list'),
    path('pandas/', views.pandas, name='pandas'),
    path('', views.MachineListView.as_view(), name='machine_list'),
]
