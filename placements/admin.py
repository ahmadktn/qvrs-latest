from django.contrib import admin
from placements.models import PlacementRequest, Placement

@admin.register(PlacementRequest)
class PlacementRequestAdmin(admin.ModelAdmin):
    list_display = ('student', 'organization', 'status', 'proposed_start_date', 'created_at')
    list_filter = ('status',)
    search_fields = ('student__registration_number', 'student__user__username', 'organization__name')

@admin.register(Placement)
class PlacementAdmin(admin.ModelAdmin):
    list_display = ('student', 'organization', 'academic_supervisor', 'status', 'start_date', 'end_date', 'completion_date')
    list_filter = ('status',)
    search_fields = ('student__registration_number', 'organization__name', 'academic_supervisor__username')
