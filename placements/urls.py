from django.urls import path
from placements import views

urlpatterns = [
    path('placements/request/<int:org_id>/', views.student_request_placement_view, name='student_request_placement'),
    path('student/my-placements/', views.student_placements_list_view, name='student_placements'),
    path('coordinator/placements/', views.coordinator_placements_queue_view, name='coordinator_placements_queue'),
    path('coordinator/placements/process/<int:request_id>/', views.coordinator_process_placement_view, name='coordinator_process_placement'),
    path('placements/complete/<int:placement_id>/', views.mark_placement_complete_view, name='mark_placement_complete'),
]
