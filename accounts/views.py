from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from accounts.forms import LoginForm, StudentRegistrationForm, SupervisorCreationForm
from accounts.models import Student
from accounts.decorators import coordinator_required

User = get_user_model()

def login_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')

    form = LoginForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f"Welcome back, {user.first_name or user.username}!")
                return redirect('dashboard')
            else:
                messages.error(request, "Invalid username/registration number or password.")
        else:
            messages.error(request, "Sign-in failed. Please check your username and password.")

    return render(request, 'accounts/login.html', {'form': form})


def student_register_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')

    form = StudentRegistrationForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            user = User.objects.create_user(
                username=form.cleaned_data['username'],
                email=form.cleaned_data['email'],
                password=form.cleaned_data['password'],
                first_name=form.cleaned_data['first_name'],
                last_name=form.cleaned_data['last_name'],
                phone_number=form.cleaned_data.get('phone_number', ''),
                role=User.Role.STUDENT
            )
            Student.objects.create(
                user=user,
                registration_number=form.cleaned_data['registration_number'],
                faculty=form.cleaned_data.get('faculty') or 'Faculty of Computing',
                department=form.cleaned_data.get('department') or 'Software Engineering',
                course_of_study=form.cleaned_data.get('course_of_study') or 'B.Sc. Software Engineering',
                level=form.cleaned_data.get('level') or '400L',
                session=form.cleaned_data.get('session') or '2025/2026'
            )
            messages.success(request, "Student registration successful! You may now sign in with your credentials.")
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
    supervisors = User.objects.filter(role=User.Role.SUPERVISOR).order_by('-created_at')
    return render(request, 'coordinator/supervisors_list.html', {
        'supervisors': supervisors,
    })


@coordinator_required
def coordinator_create_supervisor_view(request):
    form = SupervisorCreationForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            user = User.objects.create_user(
                username=form.cleaned_data['username'],
                email=form.cleaned_data['email'],
                password=form.cleaned_data['password'],
                first_name=form.cleaned_data['first_name'],
                last_name=form.cleaned_data['last_name'],
                phone_number=form.cleaned_data.get('phone_number', ''),
                role=User.Role.SUPERVISOR,
                is_staff=True
            )
            messages.success(request, f"Academic Supervisor '{user.get_full_name() or user.username}' registered successfully!")
            return redirect('coordinator_supervisors_list')
        else:
            messages.error(request, "Failed to create supervisor account. Please check the errors in the form below.")

    return render(request, 'coordinator/supervisor_create.html', {'form': form})


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
