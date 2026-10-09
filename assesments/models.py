from django.db import models
from django.conf import settings
from organisations.models import Organization
from placements.models import Placement

class SupervisorAssessment(models.Model):
    RATING_CHOICES = [
        (1, '1 - Strongly Disagree'),
        (2, '2 - Disagree'),
        (3, '3 - Neutral'),
        (4, '4 - Agree'),
        (5, '5 - Strongly Agree'),
    ]

    placement = models.OneToOneField(
        Placement,
        on_delete=models.CASCADE,
        related_name='assessment'
    )
    organization = models.ForeignKey(
        Organization,
        on_delete=models.CASCADE,
        related_name='assessments'
    )
    academic_supervisor = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='submitted_assessments'
    )
    q1_skill_relevance = models.PositiveSmallIntegerField(
        choices=RATING_CHOICES,
        help_text="Did the student gain curriculum-relevant, practical skills rather than menial tasks?"
    )
    q2_supervision_adequacy = models.PositiveSmallIntegerField(
        choices=RATING_CHOICES,
        help_text="Was the organization's technical industry supervision adequate and committed?"
    )
    q3_curriculum_alignment = models.PositiveSmallIntegerField(
        choices=RATING_CHOICES,
        help_text="Was the training genuinely aligned with the departmental Software Engineering curriculum?"
    )
    q4_recommend_future = models.PositiveSmallIntegerField(
        choices=RATING_CHOICES,
        help_text="Would you recommend this organization for future SIWES student placements?"
    )
    overall_rating = models.DecimalField(
        max_digits=3,
        decimal_places=2,
        help_text="Calculated average of Q1-Q4 (scale 1.00 to 5.00)"
    )
    qualitative_feedback = models.TextField(
        help_text="Detailed narrative of supervisor findings during assessment/visitation"
    )
    observed_student_tasks = models.TextField(
        help_text="Types of tasks student actually performed during placement"
    )
    assessed_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        # Calculate average of Q1-Q4
        total = self.q1_skill_relevance + self.q2_supervision_adequacy + self.q3_curriculum_alignment + self.q4_recommend_future
        self.overall_rating = round(total / 4.0, 2)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Assessment for {self.organization.name} by {self.academic_supervisor.get_full_name()} ({self.overall_rating} Stars)"


class OrganizationRating(models.Model):
    organization = models.OneToOneField(
        Organization,
        on_delete=models.CASCADE,
        related_name='rating_summary'
    )
    total_assessments = models.PositiveIntegerField(default=0)
    average_rating = models.DecimalField(max_digits=3, decimal_places=2, default=0.00)
    avg_skill_relevance = models.DecimalField(max_digits=3, decimal_places=2, default=0.00)
    avg_supervision_adequacy = models.DecimalField(max_digits=3, decimal_places=2, default=0.00)
    avg_curriculum_alignment = models.DecimalField(max_digits=3, decimal_places=2, default=0.00)
    avg_recommendation = models.DecimalField(max_digits=3, decimal_places=2, default=0.00)
    last_calculated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.organization.name}: {self.average_rating} Stars ({self.total_assessments} assessments)"


class OrganizationReview(models.Model):
    class Status(models.TextChoices):
        PENDING = 'PENDING', 'Pending Review'
        REVIEWED = 'REVIEWED', 'Reviewed & Resolved'

    class Outcome(models.TextChoices):
        RETAIN_APPROVAL = 'RETAIN_APPROVAL', 'Retain Approval (Warning Issued)'
        PLACE_ON_MONITORING = 'PLACE_ON_MONITORING', 'Place Under Formal Monitoring'
        REQUIRE_FURTHER_ASSESSMENT = 'REQUIRE_FURTHER_ASSESSMENT', 'Require Further Assessment'
        BLACKLIST = 'BLACKLIST', 'Blacklist Organization'

    organization = models.ForeignKey(
        Organization,
        on_delete=models.CASCADE,
        related_name='flag_reviews'
    )
    triggered_by_rating = models.DecimalField(max_digits=3, decimal_places=2)
    flag_reason = models.TextField(
        default="Average supervisor assessment score fell below departmental minimum threshold of 3.00/5.00."
    )
    flagged_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.PENDING
    )
    reviewed_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='conducted_flag_reviews'
    )
    outcome = models.CharField(
        max_length=30,
        choices=Outcome.choices,
        null=True,
        blank=True
    )
    review_notes = models.TextField(blank=True)
    resolved_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"Flag Review: {self.organization.name} ({self.triggered_by_rating} Stars) - {self.get_status_display()}"


class BlacklistRecord(models.Model):
    organization = models.OneToOneField(
        Organization,
        on_delete=models.CASCADE,
        related_name='blacklist_record'
    )
    review = models.ForeignKey(
        OrganizationReview,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='blacklist_actions'
    )
    blacklisted_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name='blacklisted_organizations'
    )
    reason = models.TextField()
    blacklisted_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"Blacklist Record: {self.organization.name}"
