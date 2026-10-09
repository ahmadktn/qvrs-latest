from django.db import models
from django.conf import settings
from django.core.exceptions import ValidationError
from accounts.models import Student
from organisations.models import Organization, TrainingOpportunity

class PlacementRequest(models.Model):
    class Status(models.TextChoices):
        PENDING = 'PENDING', 'Pending Departmental Approval'
        ACCEPTED = 'ACCEPTED', 'Accepted & Approved'
        REJECTED = 'REJECTED', 'Rejected by Coordinator'
        CANCELLED = 'CANCELLED', 'Cancelled by Student'

    student = models.ForeignKey(
        Student,
        on_delete=models.CASCADE,
        related_name='placement_requests'
    )
    organization = models.ForeignKey(
        Organization,
        on_delete=models.CASCADE,
        related_name='placement_requests'
    )
    training_opportunity = models.ForeignKey(
        TrainingOpportunity,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    proposed_start_date = models.DateField()
    proposed_end_date = models.DateField()
    cover_note = models.TextField(blank=True)
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.PENDING
    )
    coordinator_feedback = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def clean(self):
        super().clean()
        if self.organization:
            if self.organization.status == Organization.Status.BLACKLISTED:
                raise ValidationError("Placement requests cannot be submitted to a blacklisted organization.")
            if self.organization.status not in [Organization.Status.APPROVED, Organization.Status.ACTIVE, Organization.Status.REVIEWED]:
                raise ValidationError("Placement requests can only be submitted to approved host organizations.")

    def __str__(self):
        return f"{self.student.registration_number} -> {self.organization.name} ({self.get_status_display()})"


class Placement(models.Model):
    class Status(models.TextChoices):
        ONGOING = 'ONGOING', 'Ongoing / Active'
        COMPLETED = 'COMPLETED', 'Completed'
        TERMINATED = 'TERMINATED', 'Terminated Early'

    placement_request = models.OneToOneField(
        PlacementRequest,
        on_delete=models.CASCADE,
        related_name='placement'
    )
    student = models.ForeignKey(
        Student,
        on_delete=models.CASCADE,
        related_name='placements'
    )
    organization = models.ForeignKey(
        Organization,
        on_delete=models.CASCADE,
        related_name='placements'
    )
    academic_supervisor = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='supervised_placements'
    )
    start_date = models.DateField()
    end_date = models.DateField()
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.ONGOING
    )
    completion_date = models.DateField(null=True, blank=True)
    marked_completed_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='completed_placements'
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Placement: {self.student.registration_number} @ {self.organization.name} ({self.get_status_display()})"
