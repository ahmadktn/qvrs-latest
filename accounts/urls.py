from django.urls import path
from accounts import views

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('register/student/', views.student_register_view, name='register_student'),
    path('dashboard/', views.dashboard_dispatcher_view, name='dashboard'),
    path('coordinator/supervisors/', views.coordinator_supervisors_list_view, name='coordinator_supervisors_list'),
    path('coordinator/supervisors/<int:supervisor_id>/', views.coordinator_supervisor_detail_view, name='coordinator_supervisor_detail'),
    path('coordinator/supervisors/create/', views.coordinator_create_supervisor_view, name='coordinator_create_supervisor'),
    path('coordinator/supervisors/assign/', views.coordinator_assign_supervisor_view, name='coordinator_assign_supervisor'),
    path('coordinator/supervisors/unassign/<int:placement_id>/', views.coordinator_unassign_supervisor_view, name='coordinator_unassign_supervisor'),
]
