from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.db import transaction

from accounts.decorators import student_required, coordinator_required
from organisations.models import Organization
from placements.models import PlacementRequest, Placement
from placements.forms import PlacementRequestForm, CoordinatorPlacementProcessForm

@student_required
def student_request_placement_view(request, org_id):
    org = get_object_or_404(Organization, id=org_id)
    student = request.user.student_profile

    # Gatekeeping Validation (Section 6.2 & Chapter 3 FRs)
    if org.status == Organization.Status.BLACKLISTED:
        messages.error(request, "CRITICAL: Placement requests cannot be submitted to blacklisted organizations.")
        return redirect('approved_directory')

    if not org.is_approved_for_placement:
        messages.error(request, "Placement requests can only be submitted to approved host organizations.")
        return redirect('approved_directory')

    # Prevent duplicate pending requests to same org
    if PlacementRequest.objects.filter(student=student, organization=org, status=PlacementRequest.Status.PENDING).exists():
        messages.warning(request, "You already have a pending placement request for this organization.")
        return redirect('student_placements')

    form = PlacementRequestForm(request.POST or None, organization=org)
    if request.method == 'POST' and form.is_valid():
        placement_req = form.save(commit=False)
        placement_req.student = student
        placement_req.organization = org
        placement_req.status = PlacementRequest.Status.PENDING
        placement_req.save()

        messages.success(request, f"Your placement request to '{org.name}' has been submitted for SIWES Coordinator review!")
        return redirect('student_placements')

    return render(request, 'placements/request_form.html', {
        'org': org,
        'form': form,
    })


@student_required
def student_placements_list_view(request):
    student = request.user.student_profile
    requests_list = PlacementRequest.objects.filter(student=student).select_related('organization', 'training_opportunity').order_by('-created_at')
    active_placements = Placement.objects.filter(student=student).select_related('organization', 'academic_supervisor').order_by('-created_at')

    return render(request, 'student/placement_history.html', {
        'student': student,
        'requests_list': requests_list,
        'active_placements': active_placements,
    })


@coordinator_required
def coordinator_placements_queue_view(request):
    pending_requests = PlacementRequest.objects.filter(status=PlacementRequest.Status.PENDING).select_related('student', 'organization', 'student__user', 'training_opportunity')
    all_placements = Placement.objects.select_related('student', 'organization', 'academic_supervisor', 'student__user').order_by('-created_at')

    return render(request, 'placements/coordinator_queue.html', {
        'pending_requests': pending_requests,
        'all_placements': all_placements,
    })


@coordinator_required
def coordinator_process_placement_view(request, request_id):
    placement_req = get_object_or_404(PlacementRequest, id=request_id)
    form = CoordinatorPlacementProcessForm(request.POST or None)

    if request.method == 'POST' and form.is_valid():
        status_choice = form.cleaned_data['status']
        supervisor = form.cleaned_data['academic_supervisor']
        feedback = form.cleaned_data['coordinator_feedback']

        with transaction.atomic():
            placement_req.status = status_choice
            placement_req.coordinator_feedback = feedback
            placement_req.save()

            if status_choice == PlacementRequest.Status.ACCEPTED:
                # Create Placement
                Placement.objects.create(
                    placement_request=placement_req,
                    student=placement_req.student,
                    organization=placement_req.organization,
                    academic_supervisor=supervisor,
                    start_date=placement_req.proposed_start_date,
                    end_date=placement_req.proposed_end_date,
                    status=Placement.Status.ONGOING
                )
                messages.success(request, f"Placement request for {placement_req.student.registration_number} ACCEPTED & placement created!")
            else:
                messages.warning(request, f"Placement request for {placement_req.student.registration_number} REJECTED.")

        return redirect('coordinator_placements_queue')

    return render(request, 'placements/process_request_modal.html', {
        'placement_req': placement_req,
        'form': form,
    })


@login_required
def mark_placement_complete_view(request, placement_id):
    placement = get_object_or_404(Placement, id=placement_id)

    # Permission check: Coordinator or assigned supervisor
    if not (request.user.is_coordinator or request.user == placement.academic_supervisor):
        messages.error(request, "Permission denied.")
        return redirect('dashboard')

    if request.method == 'POST':
        placement.status = Placement.Status.COMPLETED
        placement.completion_date = timezone.now().date()
        placement.marked_completed_by = request.user
        placement.save()

        messages.success(request, f"Placement for {placement.student.registration_number} at '{placement.organization.name}' marked as COMPLETED! Post-placement supervisor assessment is now required.")

    return redirect('coordinator_placements_queue' if request.user.is_coordinator else 'supervisor_assessments')
