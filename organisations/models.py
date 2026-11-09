from django.db import models
from django.conf import settings

class Organization(models.Model):
    class Status(models.TextChoices):
        SUBMITTED = 'SUBMITTED', 'Submitted'
        UNDER_REVIEW = 'UNDER_REVIEW', 'Under Review'
        APPROVED = 'APPROVED', 'Approved'
        REJECTED = 'REJECTED', 'Rejected'
        ACTIVE = 'ACTIVE', 'Active'
        FLAGGED = 'FLAGGED', 'Flagged for Low Rating'
        REVIEWED = 'REVIEWED', 'Reviewed'
        BLACKLISTED = 'BLACKLISTED', 'Blacklisted'

    name = models.CharField(max_length=255, unique=True)
    registration_number = models.CharField(max_length=100, blank=True, help_text="e.g., CAC RC Number")
    industry_sector = models.CharField(max_length=100, help_text="e.g., Software Development, FinTech, Telecom")
    services_provided = models.TextField(help_text="Detailed description of core business operations")
    address = models.TextField(help_text="Physical corporate address")
    city = models.CharField(max_length=100, default='Kano')
    local_government = models.CharField(max_length=100, default='', verbose_name="Local Government", help_text="Local Government Area (LGA)")
    state = models.CharField(max_length=100, default='Kano')
    website = models.URLField(blank=True)
    contact_person_name = models.CharField(max_length=150)
    contact_person_email = models.EmailField()
    contact_person_phone = models.CharField(max_length=30)
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.SUBMITTED
    )
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='created_organizations'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} ({self.get_status_display()})"

    @property
    def is_approved_for_placement(self):
        return self.status in [self.Status.APPROVED, self.Status.ACTIVE, self.Status.REVIEWED] and self.status != self.Status.BLACKLISTED


class TrainingOpportunity(models.Model):
    organization = models.ForeignKey(
        Organization,
        on_delete=models.CASCADE,
        related_name='training_opportunities'
    )
    role_title = models.CharField(max_length=200)
    role_description = models.TextField(help_text="Specific day-to-day training tasks and responsibilities")
    expected_skills = models.TextField(help_text="Technical/engineering skills student will acquire")
    curriculum_relevance_notes = models.TextField(blank=True, help_text="Alignment with Software Engineering curriculum")
    slots_available = models.PositiveIntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.role_title} at {self.organization.name}"


class OrganizationVetting(models.Model):
    class Decision(models.TextChoices):
        APPROVED = 'APPROVED', 'Approved'
        REJECTED = 'REJECTED', 'Rejected'
        NEEDS_CLARIFICATION = 'NEEDS_CLARIFICATION', 'Needs Clarification'

    SCORE_CHOICES = [(i, f"{i} Star{'s' if i > 1 else ''}") for i in range(1, 6)]

    organization = models.ForeignKey(
        Organization,
        on_delete=models.CASCADE,
        related_name='vetting_records'
    )
    vetted_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='conducted_vettings'
    )
    decision = models.CharField(max_length=20, choices=Decision.choices)
    core_business_match_score = models.PositiveSmallIntegerField(choices=SCORE_CHOICES)
    training_role_suitability_score = models.PositiveSmallIntegerField(choices=SCORE_CHOICES)
    capacity_assessment = models.TextField()
    coordinator_comments = models.TextField()
    vetted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Vetting for {self.organization.name} - {self.get_decision_display()}"
