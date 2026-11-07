from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from accounts.forms import LoginForm, StudentRegistrationForm, SupervisorCreationForm
from accounts.models import Student
from accounts.decorators import coordinator_required
from placements.models import Placement

User = get_user_model()

def login_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')

    form = LoginForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            login_id = form.cleaned_data.get('login_id', '').strip()
            password = form.cleaned_data.get('password')

            # Lookup by email, registration number, or username
            user_obj = User.objects.filter(email__iexact=login_id).first()
            if not user_obj:
                student_profile = Student.objects.filter(registration_number__iexact=login_id).first()
                if student_profile:
                    user_obj = student_profile.user
            if not user_obj:
                user_obj = User.objects.filter(username__iexact=login_id).first()

            username_to_auth = user_obj.username if user_obj else login_id
            user = authenticate(request, username=username_to_auth, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f"Welcome back, {user.first_name or user.username}!")
                return redirect('dashboard')
            else:
                messages.error(request, "Invalid email / registration number or password.")
        else:
            messages.error(request, "Sign-in failed. Please check your credentials.")

    return render(request, 'accounts/login.html', {'form': form})


def register_hub_view(request):
    role = request.GET.get('role', 'student')
    if role == 'supervisor':
        return redirect('register_supervisor')
    return redirect('register_student')


def supervisor_register_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')

    form = SupervisorCreationForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            full_name = form.cleaned_data['full_name'].strip()
            email = form.cleaned_data['email'].strip().lower()
            state = form.cleaned_data['state'].strip()
            password = form.cleaned_data['password']

            user = User.objects.create_user(
                username=email,
                email=email,
                password=password,
                first_name=full_name,
                last_name='',
                state=state,
                role=User.Role.SUPERVISOR,
                is_staff=True
            )
            messages.success(request, f"Academic Supervisor account registered successfully! You may now sign in with your email ({email}).")
            return redirect('login')
        else:
            detailed_errors = []
            for field, errors in form.errors.items():
                for err in errors:
                    field_name = form.fields[field].label if field in form.fields and form.fields[field].label else field.replace('_', ' ').title()
                    detailed_errors.append(f"{field_name}: {err}")
            
            error_message = "Registration Failed: " + "; ".join(detailed_errors)
            messages.error(request, error_message)

    return render(request, 'accounts/register_supervisor.html', {'form': form})


def student_register_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')

    form = StudentRegistrationForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            reg_num = form.cleaned_data['registration_number'].strip().upper()
            email = form.cleaned_data['email'].strip().lower()
            full_name = form.cleaned_data['full_name'].strip()
            password = form.cleaned_data['password']

            # Use registration number as unique username
            user = User.objects.create_user(
                username=reg_num,
                email=email,
                password=password,
                first_name=full_name,
                last_name='',
                role=User.Role.STUDENT
            )
            Student.objects.create(
                user=user,
                registration_number=reg_num,
                faculty='Faculty of Computing',
                department='Software Engineering',
                course_of_study='B.Sc. Software Engineering',
                level='400L',
                session='2025/2026'
            )
            messages.success(request, "Student registration successful! You may now sign in with your email or registration number.")
            return redirect('login')
        else:
            detailed_errors = []
            for field, errors in form.errors.items():
                for err in errors:
                    field_name = form.fields[field].label if field in form.fields and form.fields[field].label else field.replace('_', ' ').title()
                    detailed_errors.append(f"{field_name}: {err}")
            
            error_message = "Registration Failed: " + "; ".join(detailed_errors)
            messages.error(request, error_message)

    return render(request, 'accounts/register_student.html', {'form': form})


@coordinator_required
def coordinator_supervisors_list_view(request):
    supervisors = User.objects.filter(role=User.Role.SUPERVISOR).prefetch_related(
        'supervised_placements__student__user',
        'supervised_placements__organization'
    ).order_by('-created_at')

    # Placements available for assignment (ongoing placements)
    available_placements = Placement.objects.filter(
        status=Placement.Status.ONGOING
    ).select_related('student__user', 'organization', 'academic_supervisor').order_by('organization__state', 'student__registration_number')

    return render(request, 'coordinator/supervisors_list.html', {
        'supervisors': supervisors,
        'available_placements': available_placements,
    })


@coordinator_required
def coordinator_create_supervisor_view(request):
    form = SupervisorCreationForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            full_name = form.cleaned_data['full_name'].strip()
            email = form.cleaned_data['email'].strip().lower()
            state = form.cleaned_data['state'].strip()
            password = form.cleaned_data['password']

            user = User.objects.create_user(
                username=email,
                email=email,
                password=password,
                first_name=full_name,
                last_name='',
                state=state,
                role=User.Role.SUPERVISOR,
                is_staff=True
            )
            messages.success(request, f"Academic Supervisor '{full_name}' assigned to state '{state}' registered successfully!")
            return redirect('coordinator_supervisors_list')
        else:
            messages.error(request, "Failed to create supervisor account. Please check the errors in the form below.")

    return render(request, 'coordinator/supervisor_create.html', {'form': form})


@coordinator_required
def coordinator_supervisor_detail_view(request, supervisor_id):
    supervisor = get_object_or_404(User, id=supervisor_id, role=User.Role.SUPERVISOR)
    supervised_placements = supervisor.supervised_placements.select_related(
        'student__user',
        'organization',
        'placement_request'
    ).order_by('-created_at')

    available_placements = Placement.objects.filter(
        status=Placement.Status.ONGOING
    ).exclude(academic_supervisor=supervisor).select_related('student__user', 'organization', 'academic_supervisor').order_by('organization__state', 'student__registration_number')

    return render(request, 'coordinator/supervisor_detail.html', {
        'supervisor': supervisor,
        'supervised_placements': supervised_placements,
        'available_placements': available_placements,
    })


@coordinator_required
def coordinator_assign_supervisor_view(request):
    next_url = request.POST.get('next') or 'coordinator_supervisors_list'
    if request.method == 'POST':
        supervisor_id = request.POST.get('supervisor_id')
        placement_id = request.POST.get('placement_id')

        supervisor = get_object_or_404(User, id=supervisor_id, role=User.Role.SUPERVISOR)
        placement = get_object_or_404(Placement, id=placement_id)

        placement.academic_supervisor = supervisor
        placement.save()

        messages.success(
            request,
            f"Successfully assigned Student {placement.student.registration_number} ({placement.student.user.first_name}) at '{placement.organization.name}' ({placement.organization.state}) to Supervisor {supervisor.first_name}."
        )

    return redirect(next_url)


@coordinator_required
def coordinator_unassign_supervisor_view(request, placement_id):
    next_url = request.POST.get('next') or 'coordinator_supervisors_list'
    if request.method == 'POST':
        placement = get_object_or_404(Placement, id=placement_id)
        prev_sup = placement.academic_supervisor
        placement.academic_supervisor = None
        placement.save()

        messages.info(
            request,
            f"Unassigned Student {placement.student.registration_number} from supervisor {prev_sup.first_name if prev_sup else ''}."
        )

    return redirect(next_url)


def logout_view(request):
    logout(request)
    messages.info(request, "You have been signed out.")
    return redirect('home')


@login_required
def dashboard_dispatcher_view(request):
    user = request.user
    if user.is_coordinator or user.is_superuser:
        return redirect('coordinator_dashboard')
    elif user.is_supervisor:
        return redirect('supervisor_assessments')
    elif user.is_student:
        return redirect('student_placements')
    elif user.is_organization:
        return redirect('approved_directory')
    return redirect('home')
