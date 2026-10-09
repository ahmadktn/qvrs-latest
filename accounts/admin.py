from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from accounts.models import User, Student

@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'role', 'is_active', 'created_at')
    list_filter = ('role', 'is_active', 'is_staff')
    search_fields = ('username', 'email', 'first_name', 'last_name')
    fieldsets = BaseUserAdmin.fieldsets + (
        ('Role & Phone Info', {'fields': ('role', 'phone_number')}),
    )

@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('registration_number', 'user', 'department', 'level', 'session')
    search_fields = ('registration_number', 'user__username', 'user__first_name', 'user__last_name')
    list_filter = ('department', 'level', 'session')
