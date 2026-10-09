from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from accounts.forms import LoginForm, StudentRegistrationForm
from accounts.models import Student

User = get_user_model()

def login_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')

    form = LoginForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, f"Welcome back, {user.first_name or user.username}!")
            return redirect('dashboard')
        else:
            messages.error(request, "Invalid username/registration number or password.")

    return render(request, 'accounts/login.html', {'form': form})


def student_register_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')

    form = StudentRegistrationForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        user = User.objects.create_user(
            username=form.cleaned_data['username'],
            email=form.cleaned_data['email'],
            password=form.cleaned_data['password'],
            first_name=form.cleaned_data['first_name'],
            last_name=form.cleaned_data['last_name'],
            phone_number=form.cleaned_data['phone_number'],
            role=User.Role.STUDENT
        )
        Student.objects.create(
            user=user,
            registration_number=form.cleaned_data['registration_number'],
            faculty=form.cleaned_data['faculty'],
            department=form.cleaned_data['department'],
            course_of_study=form.cleaned_data['course_of_study'],
            level=form.cleaned_data['level'],
            session=form.cleaned_data['session']
        )
        messages.success(request, "Registration successful! You may now sign in.")
        return redirect('login')

    return render(request, 'accounts/register_student.html', {'form': form})


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
