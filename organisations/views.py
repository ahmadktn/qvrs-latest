from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.db.models import Q, Avg
from django.db import transaction
from django.contrib.auth.decorators import login_required

from accounts.decorators import coordinator_required
from organisations.models import Organization, TrainingOpportunity, OrganizationVetting
from organisations.forms import OrganizationSubmissionForm, TrainingOpportunityForm, OrganizationVettingForm
from placements.models import PlacementRequest, Placement
from assesments.models import SupervisorAssessment, OrganizationRating, OrganizationReview, BlacklistRecord

def home_view(request):
    featured_orgs = Organization.objects.filter(
        status__in=[Organization.Status.APPROVED, Organization.Status.ACTIVE, Organization.Status.REVIEWED]
    ).select_related('rating_summary').order_by('-rating_summary__average_rating')[:3]

    stats = {
        'total_approved': Organization.objects.filter(status__in=[Organization.Status.APPROVED, Organization.Status.ACTIVE, Organization.Status.REVIEWED]).count(),
        'total_placements': Placement.objects.filter(status=Placement.Status.COMPLETED).count(),
        'total_assessments': SupervisorAssessment.objects.count(),
    }

    return render(request, 'pages/home.html', {
        'featured_orgs': featured_orgs,
        'stats': stats,
    })


def organization_submit_view(request):
    org_form = OrganizationSubmissionForm(request.POST or None)
    role_form = TrainingOpportunityForm(request.POST or None)

    if request.method == 'POST':
        if org_form.is_valid() and role_form.is_valid():
            with transaction.atomic():
                org = org_form.save(commit=False)
                org.status = Organization.Status.SUBMITTED
                if request.user.is_authenticated:
                    org.created_by = request.user
                org.save()

                role = role_form.save(commit=False)
                role.organization = org
                role.save()

            messages.success(request, f"Organization '{org.name}' and training opportunity successfully submitted for departmental vetting!")
            return redirect('submission_status', org_id=org.id)
        else:
            messages.error(request, "Please correct the errors in the form below.")

    return render(request, 'organisations/organization_submit.html', {
        'org_form': org_form,
        'role_form': role_form,
    })


def submission_status_view(request, org_id):
    org = get_object_or_404(Organization, id=org_id)
    vetting_record = org.vetting_records.last()
    opportunities = org.training_opportunities.all()

    return render(request, 'organisations/submission_status.html', {
        'org': org,
        'vetting_record': vetting_record,
        'opportunities': opportunities,
    })


def approved_directory_view(request):
    # Query ONLY approved, non-blacklisted organizations
    query = request.GET.get('q', '').strip()
    sector = request.GET.get('sector', '').strip()
    min_stars = request.GET.get('stars', '').strip()
    sort_by = request.GET.get('sort', 'rating_desc').strip()

    orgs = Organization.objects.filter(
        status__in=[Organization.Status.APPROVED, Organization.Status.ACTIVE, Organization.Status.REVIEWED]
    ).exclude(status=Organization.Status.BLACKLISTED).select_related('rating_summary').prefetch_related('training_opportunities')

    if query:
        orgs = orgs.filter(
            Q(name__icontains=query) |
            Q(industry_sector__icontains=query) |
            Q(services_provided__icontains=query) |
            Q(training_opportunities__role_title__icontains=query) |
            Q(training_opportunities__expected_skills__icontains=query)
        ).distinct()

    if sector:
        orgs = orgs.filter(industry_sector__iexact=sector)

    if min_stars:
        try:
            stars_val = float(min_stars)
            orgs = orgs.filter(rating_summary__average_rating__gte=stars_val)
        except ValueError:
            pass

    if sort_by == 'rating_desc':
        orgs = orgs.order_by('-rating_summary__average_rating', 'name')
    elif sort_by == 'name_asc':
        orgs = orgs.order_by('name')
    elif sort_by == 'recent':
        orgs = orgs.order_by('-created_at')

    # Get available sectors for dynamic filter dropdown
    sectors = Organization.objects.filter(
        status__in=[Organization.Status.APPROVED, Organization.Status.ACTIVE, Organization.Status.REVIEWED]
    ).values_list('industry_sector', flat=True).distinct()

    return render(request, 'directory/approved_list.html', {
        'orgs': orgs,
        'query': query,
        'selected_sector': sector,
        'selected_stars': min_stars,
        'selected_sort': sort_by,
        'sectors': sectors,
    })


def org_detail_view(request, org_id):
    org = get_object_or_404(Organization, id=org_id)

    # Strictly block viewing if blacklisted or rejected unless coordinator
    if org.status == Organization.Status.BLACKLISTED and not (request.user.is_authenticated and request.user.is_coordinator):
        messages.error(request, "This organization has been blacklisted and is barred from the directory.")
        return redirect('approved_directory')

    rating_summary, _ = OrganizationRating.objects.get_or_create(organization=org)
    opportunities = org.training_opportunities.all()
    recent_assessments = org.assessments.select_related('academic_supervisor').order_by('-assessed_at')[:5]
    completed_placements_count = org.placements.filter(status=Placement.Status.COMPLETED).count()

    return render(request, 'directory/org_detail.html', {
        'org': org,
        'rating_summary': rating_summary,
        'opportunities': opportunities,
        'recent_assessments': recent_assessments,
        'completed_placements_count': completed_placements_count,
    })


@coordinator_required
def coordinator_dashboard_view(request):
    pending_vettings = Organization.objects.filter(status=Organization.Status.SUBMITTED).order_by('-created_at')
    approved_count = Organization.objects.filter(status__in=[Organization.Status.APPROVED, Organization.Status.ACTIVE, Organization.Status.REVIEWED]).count()
    active_placements_count = Placement.objects.filter(status=Placement.Status.ONGOING).count()
    flagged_reviews = OrganizationReview.objects.filter(status=OrganizationReview.Status.PENDING).select_related('organization', 'organization__rating_summary')
    pending_placement_requests = PlacementRequest.objects.filter(status=PlacementRequest.Status.PENDING).select_related('student', 'organization', 'student__user')

    return render(request, 'coordinator/dashboard.html', {
        'pending_vettings': pending_vettings,
        'approved_count': approved_count,
        'active_placements_count': active_placements_count,
        'flagged_reviews': flagged_reviews,
        'pending_placement_requests': pending_placement_requests,
    })


@coordinator_required
def coordinator_vetting_detail_view(request, org_id):
    org = get_object_or_404(Organization, id=org_id)
    opportunities = org.training_opportunities.all()
    past_history = {
        'placements_count': org.placements.filter(status=Placement.Status.COMPLETED).count(),
        'rating_summary': getattr(org, 'rating_summary', None)
    }

    form = OrganizationVettingForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        vetting = form.save(commit=False)
        vetting.organization = org
        vetting.vetted_by = request.user
        vetting.save()

        if vetting.decision == OrganizationVetting.Decision.APPROVED:
            org.status = Organization.Status.APPROVED
            OrganizationRating.objects.get_or_create(organization=org)
            messages.success(request, f"Organization '{org.name}' has been APPROVED and added to the Approved Directory!")
        elif vetting.decision == OrganizationVetting.Decision.REJECTED:
            org.status = Organization.Status.REJECTED
            messages.warning(request, f"Organization '{org.name}' has been REJECTED. Submitter can view coordinator feedback.")
        org.save()

        return redirect('coordinator_dashboard')

    return render(request, 'coordinator/vetting_detail.html', {
        'org': org,
        'opportunities': opportunities,
        'past_history': past_history,
        'form': form,
    })
