from django.contrib import admin
from organisations.models import Organization, TrainingOpportunity, OrganizationVetting

class TrainingOpportunityInline(admin.TabularInline):
    model = TrainingOpportunity
    extra = 1

@admin.register(Organization)
class OrganizationAdmin(admin.ModelAdmin):
    list_display = ('name', 'industry_sector', 'status', 'city', 'local_government', 'state', 'contact_person_name', 'created_at')
    list_filter = ('status', 'industry_sector', 'state', 'local_government')
    search_fields = ('name', 'industry_sector', 'services_provided', 'contact_person_name', 'local_government', 'city')
    inlines = [TrainingOpportunityInline]

@admin.register(TrainingOpportunity)
class TrainingOpportunityAdmin(admin.ModelAdmin):
    list_display = ('role_title', 'organization', 'slots_available', 'created_at')
    search_fields = ('role_title', 'organization__name', 'expected_skills')

@admin.register(OrganizationVetting)
class OrganizationVettingAdmin(admin.ModelAdmin):
    list_display = ('organization', 'decision', 'vetted_by', 'core_business_match_score', 'training_role_suitability_score', 'vetted_at')
    list_filter = ('decision',)
    search_fields = ('organization__name', 'coordinator_comments')
