from django.contrib import admin
from assesments.models import SupervisorAssessment, OrganizationRating, OrganizationReview, BlacklistRecord

@admin.register(SupervisorAssessment)
class SupervisorAssessmentAdmin(admin.ModelAdmin):
    list_display = ('organization', 'placement', 'academic_supervisor', 'overall_rating', 'assessed_at')
    list_filter = ('overall_rating',)
    search_fields = ('organization__name', 'academic_supervisor__username', 'qualitative_feedback', 'observed_student_tasks')

@admin.register(OrganizationRating)
class OrganizationRatingAdmin(admin.ModelAdmin):
    list_display = ('organization', 'average_rating', 'total_assessments', 'avg_skill_relevance', 'avg_supervision_adequacy', 'last_calculated_at')
    search_fields = ('organization__name',)

@admin.register(OrganizationReview)
class OrganizationReviewAdmin(admin.ModelAdmin):
    list_display = ('organization', 'triggered_by_rating', 'status', 'outcome', 'reviewed_by', 'flagged_at')
    list_filter = ('status', 'outcome')
    search_fields = ('organization__name', 'flag_reason', 'review_notes')

@admin.register(BlacklistRecord)
class BlacklistRecordAdmin(admin.ModelAdmin):
    list_display = ('organization', 'blacklisted_by', 'blacklisted_at', 'is_active')
    search_fields = ('organization__name', 'reason')
