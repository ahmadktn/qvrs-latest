from django.urls import path
from organisations import views

urlpatterns = [
    path('', views.home_view, name='home'),
    path('organizations/submit/', views.organization_submit_view, name='organization_submit'),
    path('organizations/status/<int:org_id>/', views.submission_status_view, name='submission_status'),
    path('directory/', views.approved_directory_view, name='approved_directory'),
    path('directory/<int:org_id>/', views.org_detail_view, name='org_detail'),
    path('coordinator/dashboard/', views.coordinator_dashboard_view, name='coordinator_dashboard'),
    path('coordinator/vetting/<int:org_id>/', views.coordinator_vetting_detail_view, name='coordinator_vetting_detail'),
]
