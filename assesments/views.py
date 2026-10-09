from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.utils import timezone
from django.db import transaction

from accounts.decorators import supervisor_required, coordinator_required
from placements.models import Placement
from organisations.models import Organization
from assesments.models import SupervisorAssessment, OrganizationRating, OrganizationReview, BlacklistRecord
from assesments.forms import SupervisorAssessmentForm, DepartmentalReviewForm, BlacklistActionForm
from assesments.services import LowRatingDetectorService, RatingAggregationService

@supervisor_required
def supervisor_assessments_list_view(request):
    supervisor = request.user
    
    # Placements assigned to supervisor that are COMPLETED but not yet assessed
    pending_assessments = Placement.objects.filter(
        academic_supervisor=supervisor,
        status=Placement.Status.COMPLETED,
        assessment__isnull=True
    ).select_related('student', 'organization', 'student__user').order_by('-completion_date')

    # Already submitted assessments by supervisor
    completed_assessments = SupervisorAssessment.objects.filter(
        academic_supervisor=supervisor
    ).select_related('placement', 'organization', 'placement__student', 'placement__student__user').order_by('-assessed_at')

    return render(request, 'supervisor/assessment_list.html', {
        'pending_assessments': pending_assessments,
        'completed_assessments': completed_assessments,
    })


@supervisor_required
def submit_supervisor_assessment_view(request, placement_id):
    placement = get_object_or_404(Placement, id=placement_id)

    if placement.academic_supervisor != request.user and not request.user.is_superuser:
        messages.error(request, "You are not the assigned academic supervisor for this placement.")
        return redirect('supervisor_assessments')

    if hasattr(placement, 'assessment'):
        messages.warning(request, "An assessment has already been submitted for this placement.")
        return redirect('supervisor_assessments')

    form = SupervisorAssessmentForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        with transaction.atomic():
            assessment = form.save(commit=False)
            assessment.placement = placement
            assessment.organization = placement.organization
            assessment.academic_supervisor = request.user
            assessment.save()

            # Trigger rating recalculation & low-rating detector service
            flagged, rating_summary = LowRatingDetectorService.check_and_flag(placement.organization)

        if flagged:
            messages.warning(
                request,
                f"Assessment recorded! WARNING: Organization '{placement.organization.name}' average rating ({rating_summary.average_rating}/5.00) has fallen below the 3.00 threshold and has been FLAGGED for departmental review."
            )
        else:
            messages.success(
                request,
                f"Assessment recorded successfully! Updated running average for '{placement.organization.name}' is {rating_summary.average_rating} Stars ({rating_summary.total_assessments} assessments)."
            )

        return redirect('supervisor_assessments')

    return render(request, 'supervisor/assessment_form.html', {
        'placement': placement,
        'form': form,
    })


@coordinator_required
def coordinator_flagged_list_view(request):
    pending_reviews = OrganizationReview.objects.filter(
        status=OrganizationReview.Status.PENDING
    ).select_related('organization', 'organization__rating_summary').order_by('-flagged_at')

    resolved_reviews = OrganizationReview.objects.filter(
        status=OrganizationReview.Status.REVIEWED
    ).select_related('organization', 'reviewed_by').order_by('-resolved_at')

    return render(request, 'coordinator/flagged_reviews_list.html', {
        'pending_reviews': pending_reviews,
        'resolved_reviews': resolved_reviews,
    })


@coordinator_required
def coordinator_review_flagged_org_view(request, review_id):
    review = get_object_or_404(OrganizationReview, id=review_id)
    org = review.organization
    rating_summary = getattr(org, 'rating_summary', None)
    assessments_history = org.assessments.select_related('academic_supervisor', 'placement__student', 'placement__student__user').order_by('-assessed_at')

    form = DepartmentalReviewForm(request.POST or None, instance=review)
    if request.method == 'POST' and form.is_valid():
        with transaction.atomic():
            rev = form.save(commit=False)
            rev.status = OrganizationReview.Status.REVIEWED
            rev.reviewed_by = request.user
            rev.resolved_at = timezone.now()
            rev.save()

            if rev.outcome == OrganizationReview.Outcome.BLACKLIST:
                org.status = Organization.Status.BLACKLISTED
                org.save()
                BlacklistRecord.objects.create(
                    organization=org,
                    review=rev,
                    blacklisted_by=request.user,
                    reason=rev.review_notes or rev.flag_reason
                )
                messages.error(request, f"Organization '{org.name}' has been BLACKLISTED and removed from the Approved Directory!")
            elif rev.outcome in [OrganizationReview.Outcome.RETAIN_APPROVAL, OrganizationReview.Outcome.PLACE_ON_MONITORING]:
                org.status = Organization.Status.REVIEWED
                org.save()
                messages.info(request, f"Departmental review resolved: '{org.name}' retained approval with status '{org.get_status_display()}'.")
            else:
                messages.warning(request, f"Departmental review updated for '{org.name}'.")

        return redirect('coordinator_flagged_reviews')

    return render(request, 'coordinator/flag_review_detail.html', {
        'review': review,
        'org': org,
        'rating_summary': rating_summary,
        'assessments_history': assessments_history,
        'form': form,
    })


@coordinator_required
def blacklist_registry_view(request):
    blacklisted_records = BlacklistRecord.objects.select_related('organization', 'blacklisted_by', 'review').order_by('-blacklisted_at')

    return render(request, 'coordinator/blacklist_registry.html', {
        'blacklisted_records': blacklisted_records,
    })
