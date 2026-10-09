from functools import wraps
from django.contrib import messages
from django.shortcuts import redirect
from accounts.models import User

def role_required(allowed_roles):
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            if not request.user.is_authenticated:
                messages.error(request, "Please sign in to access this page.")
                return redirect('login')
            if request.user.is_superuser or request.user.role in allowed_roles:
                return view_func(request, *args, **kwargs)
            messages.error(request, "You do not have permission to access this area.")
            return redirect('dashboard')
        return _wrapped_view
    return decorator

def coordinator_required(view_func):
    return role_required([User.Role.COORDINATOR])(view_func)

def supervisor_required(view_func):
    return role_required([User.Role.SUPERVISOR])(view_func)

def student_required(view_func):
    return role_required([User.Role.STUDENT])(view_func)

def organization_required(view_func):
    return role_required([User.Role.ORGANIZATION])(view_func)
