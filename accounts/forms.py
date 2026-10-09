from django import forms
from django.contrib.auth import get_user_model
from accounts.models import Student

User = get_user_model()

class LoginForm(forms.Form):
    username = forms.CharField(
        label='Username / Reg Number',
        widget=forms.TextInput(attrs={
            'class': 'w-full px-4 py-2.5 rounded-lg border border-slate-300 focus:ring-2 focus:ring-blue-600 focus:border-transparent text-slate-800 text-sm placeholder-slate-400',
            'placeholder': 'Enter your username or reg number'
        })
    )
    password = forms.CharField(
        label='Password',
        widget=forms.PasswordInput(attrs={
            'class': 'w-full px-4 py-2.5 rounded-lg border border-slate-300 focus:ring-2 focus:ring-blue-600 focus:border-transparent text-slate-800 text-sm placeholder-slate-400 pr-10',
            'placeholder': 'Enter your password',
            'id': 'id_login_password'
        })
    )


class StudentRegistrationForm(forms.Form):
    first_name = forms.CharField(
        label='First Name',
        max_length=150,
        widget=forms.TextInput(attrs={
            'class': 'w-full px-4 py-2.5 rounded-lg border border-slate-300 focus:ring-2 focus:ring-blue-600 focus:border-transparent text-slate-800 text-sm',
            'placeholder': 'First Name'
        })
    )
    last_name = forms.CharField(
        label='Last Name',
        max_length=150,
        widget=forms.TextInput(attrs={
            'class': 'w-full px-4 py-2.5 rounded-lg border border-slate-300 focus:ring-2 focus:ring-blue-600 focus:border-transparent text-slate-800 text-sm',
            'placeholder': 'Last Name'
        })
    )
    username = forms.CharField(
        label='Username',
        max_length=150,
        widget=forms.TextInput(attrs={
            'class': 'w-full px-4 py-2.5 rounded-lg border border-slate-300 focus:ring-2 focus:ring-blue-600 focus:border-transparent text-slate-800 text-sm',
            'placeholder': 'e.g. cst20swe00123'
        })
    )
    email = forms.EmailField(
        label='BUK Email Address',
        widget=forms.EmailInput(attrs={
            'class': 'w-full px-4 py-2.5 rounded-lg border border-slate-300 focus:ring-2 focus:ring-blue-600 focus:border-transparent text-slate-800 text-sm',
            'placeholder': 'student@student.buk.edu.ng'
        })
    )
    registration_number = forms.CharField(
        label='BUK Registration Number',
        max_length=30,
        widget=forms.TextInput(attrs={
            'class': 'w-full px-4 py-2.5 rounded-lg border border-slate-300 focus:ring-2 focus:ring-blue-600 focus:border-transparent text-slate-800 text-sm',
            'placeholder': 'CST/20/SWE/00123'
        })
    )
    phone_number = forms.CharField(
        label='Phone Number',
        max_length=20,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'w-full px-4 py-2.5 rounded-lg border border-slate-300 focus:ring-2 focus:ring-blue-600 focus:border-transparent text-slate-800 text-sm',
            'placeholder': '+234 800 000 0000'
        })
    )
    faculty = forms.CharField(
        label='Faculty',
        initial='Faculty of Computing',
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'w-full px-4 py-2.5 rounded-lg border border-slate-300 focus:ring-2 focus:ring-blue-600 focus:border-transparent text-slate-800 text-sm'
        })
    )
    department = forms.CharField(
        label='Department',
        initial='Software Engineering',
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'w-full px-4 py-2.5 rounded-lg border border-slate-300 focus:ring-2 focus:ring-blue-600 focus:border-transparent text-slate-800 text-sm'
        })
    )
    course_of_study = forms.CharField(
        label='Course of Study',
        initial='B.Sc. Software Engineering',
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'w-full px-4 py-2.5 rounded-lg border border-slate-300 focus:ring-2 focus:ring-blue-600 focus:border-transparent text-slate-800 text-sm'
        })
    )
    level = forms.CharField(
        label='Academic Level',
        initial='400L',
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'w-full px-4 py-2.5 rounded-lg border border-slate-300 focus:ring-2 focus:ring-blue-600 focus:border-transparent text-slate-800 text-sm'
        })
    )
    session = forms.CharField(
        label='SIWES Session',
        initial='2025/2026',
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'w-full px-4 py-2.5 rounded-lg border border-slate-300 focus:ring-2 focus:ring-blue-600 focus:border-transparent text-slate-800 text-sm'
        })
    )
    password = forms.CharField(
        label='Password',
        widget=forms.PasswordInput(attrs={
            'class': 'w-full px-4 py-2.5 rounded-lg border border-slate-300 focus:ring-2 focus:ring-blue-600 focus:border-transparent text-slate-800 text-sm pr-10',
            'placeholder': 'Create strong password',
            'id': 'id_reg_password'
        })
    )
    confirm_password = forms.CharField(
        label='Confirm Password',
        widget=forms.PasswordInput(attrs={
            'class': 'w-full px-4 py-2.5 rounded-lg border border-slate-300 focus:ring-2 focus:ring-blue-600 focus:border-transparent text-slate-800 text-sm pr-10',
            'placeholder': 'Confirm password',
            'id': 'id_confirm_password'
        })
    )

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError("This username is already registered in the system.")
        return username

    def clean_registration_number(self):
        reg_num = self.cleaned_data.get('registration_number')
        if Student.objects.filter(registration_number=reg_num).exists():
            raise forms.ValidationError("This registration number is already registered in the system.")
        return reg_num

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password and confirm_password and password != confirm_password:
            self.add_error('confirm_password', "Passwords do not match. Please enter the same password in both fields.")
        return cleaned_data


class SupervisorCreationForm(forms.Form):
    first_name = forms.CharField(
        label='First Name',
        max_length=150,
        widget=forms.TextInput(attrs={
            'class': 'w-full px-4 py-2.5 rounded-lg border border-slate-300 focus:ring-2 focus:ring-blue-600 focus:border-transparent text-slate-800 text-sm',
            'placeholder': 'e.g. Dr. Usman'
        })
    )
    last_name = forms.CharField(
        label='Last Name',
        max_length=150,
        widget=forms.TextInput(attrs={
            'class': 'w-full px-4 py-2.5 rounded-lg border border-slate-300 focus:ring-2 focus:ring-blue-600 focus:border-transparent text-slate-800 text-sm',
            'placeholder': 'e.g. Suleiman'
        })
    )
    username = forms.CharField(
        label='Username',
        max_length=150,
        widget=forms.TextInput(attrs={
            'class': 'w-full px-4 py-2.5 rounded-lg border border-slate-300 focus:ring-2 focus:ring-blue-600 focus:border-transparent text-slate-800 text-sm',
            'placeholder': 'e.g. dr_usman'
        })
    )
    email = forms.EmailField(
        label='BUK Email Address',
        widget=forms.EmailInput(attrs={
            'class': 'w-full px-4 py-2.5 rounded-lg border border-slate-300 focus:ring-2 focus:ring-blue-600 focus:border-transparent text-slate-800 text-sm',
            'placeholder': 'usman.swe@buk.edu.ng'
        })
    )
    phone_number = forms.CharField(
        label='Phone Number',
        max_length=20,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'w-full px-4 py-2.5 rounded-lg border border-slate-300 focus:ring-2 focus:ring-blue-600 focus:border-transparent text-slate-800 text-sm',
            'placeholder': '+234 800 000 0000'
        })
    )
    password = forms.CharField(
        label='Password',
        widget=forms.PasswordInput(attrs={
            'class': 'w-full px-4 py-2.5 rounded-lg border border-slate-300 focus:ring-2 focus:ring-blue-600 focus:border-transparent text-slate-800 text-sm pr-10',
            'placeholder': 'Create password for supervisor',
            'id': 'id_sup_password'
        })
    )
    confirm_password = forms.CharField(
        label='Confirm Password',
        widget=forms.PasswordInput(attrs={
            'class': 'w-full px-4 py-2.5 rounded-lg border border-slate-300 focus:ring-2 focus:ring-blue-600 focus:border-transparent text-slate-800 text-sm pr-10',
            'placeholder': 'Confirm password',
            'id': 'id_sup_confirm_password'
        })
    )

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError("This username is already taken.")
        return username

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password and confirm_password and password != confirm_password:
            self.add_error('confirm_password', "Passwords do not match.")
        return cleaned_data
