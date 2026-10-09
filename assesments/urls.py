from django.urls import path
from assesments import views

urlpatterns = [
    path('supervisor/assessments/', views.supervisor_assessments_list_view, name='supervisor_assessments'),
    path('supervisor/assessments/submit/<int:placement_id>/', views.submit_supervisor_assessment_view, name='submit_supervisor_assessment'),
    path('coordinator/reviews/', views.coordinator_flagged_list_view, name='coordinator_flagged_reviews'),
    path('coordinator/reviews/<int:review_id>/', views.coordinator_review_flagged_org_view, name='coordinator_review_flagged_org'),
    path('coordinator/blacklist/', views.blacklist_registry_view, name='blacklist_registry'),
]
