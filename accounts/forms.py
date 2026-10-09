from django import forms
from django.contrib.auth import get_user_model
from accounts.models import Student

User = get_user_model()

class LoginForm(forms.Form):
    username = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'w-full px-4 py-2.5 rounded-lg border border-slate-300 focus:ring-2 focus:ring-blue-600 focus:border-transparent text-slate-800 text-sm placeholder-slate-400',
            'placeholder': 'Enter your username or reg number'
        })
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'w-full px-4 py-2.5 rounded-lg border border-slate-300 focus:ring-2 focus:ring-blue-600 focus:border-transparent text-slate-800 text-sm placeholder-slate-400',
            'placeholder': 'Enter your password'
        })
    )


class StudentRegistrationForm(forms.Form):
    username = forms.CharField(
        max_length=150,
        widget=forms.TextInput(attrs={
            'class': 'w-full px-4 py-2.5 rounded-lg border border-slate-300 focus:ring-2 focus:ring-blue-600 focus:border-transparent text-slate-800 text-sm',
            'placeholder': 'e.g. cst20swe00123'
        })
    )
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={
            'class': 'w-full px-4 py-2.5 rounded-lg border border-slate-300 focus:ring-2 focus:ring-blue-600 focus:border-transparent text-slate-800 text-sm',
            'placeholder': 'student@buk.edu.ng'
        })
    )
    first_name = forms.CharField(
        max_length=150,
        widget=forms.TextInput(attrs={
            'class': 'w-full px-4 py-2.5 rounded-lg border border-slate-300 focus:ring-2 focus:ring-blue-600 focus:border-transparent text-slate-800 text-sm',
            'placeholder': 'First Name'
        })
    )
    last_name = forms.CharField(
        max_length=150,
        widget=forms.TextInput(attrs={
            'class': 'w-full px-4 py-2.5 rounded-lg border border-slate-300 focus:ring-2 focus:ring-blue-600 focus:border-transparent text-slate-800 text-sm',
            'placeholder': 'Last Name'
        })
    )
    phone_number = forms.CharField(
        max_length=20,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'w-full px-4 py-2.5 rounded-lg border border-slate-300 focus:ring-2 focus:ring-blue-600 focus:border-transparent text-slate-800 text-sm',
            'placeholder': '+234 800 000 0000'
        })
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'w-full px-4 py-2.5 rounded-lg border border-slate-300 focus:ring-2 focus:ring-blue-600 focus:border-transparent text-slate-800 text-sm',
            'placeholder': 'Create strong password'
        })
    )
    registration_number = forms.CharField(
        max_length=30,
        widget=forms.TextInput(attrs={
            'class': 'w-full px-4 py-2.5 rounded-lg border border-slate-300 focus:ring-2 focus:ring-blue-600 focus:border-transparent text-slate-800 text-sm',
            'placeholder': 'CST/20/SWE/00123'
        })
    )
    faculty = forms.CharField(
        initial='Faculty of Computing',
        widget=forms.TextInput(attrs={
            'class': 'w-full px-4 py-2.5 rounded-lg border border-slate-300 focus:ring-2 focus:ring-blue-600 focus:border-transparent text-slate-800 text-sm'
        })
    )
    department = forms.CharField(
        initial='Software Engineering',
        widget=forms.TextInput(attrs={
            'class': 'w-full px-4 py-2.5 rounded-lg border border-slate-300 focus:ring-2 focus:ring-blue-600 focus:border-transparent text-slate-800 text-sm'
        })
    )
    course_of_study = forms.CharField(
        initial='B.Sc. Software Engineering',
        widget=forms.TextInput(attrs={
            'class': 'w-full px-4 py-2.5 rounded-lg border border-slate-300 focus:ring-2 focus:ring-blue-600 focus:border-transparent text-slate-800 text-sm'
        })
    )
    level = forms.CharField(
        initial='400L',
        widget=forms.TextInput(attrs={
            'class': 'w-full px-4 py-2.5 rounded-lg border border-slate-300 focus:ring-2 focus:ring-blue-600 focus:border-transparent text-slate-800 text-sm'
        })
    )
    session = forms.CharField(
        initial='2025/2026',
        widget=forms.TextInput(attrs={
            'class': 'w-full px-4 py-2.5 rounded-lg border border-slate-300 focus:ring-2 focus:ring-blue-600 focus:border-transparent text-slate-800 text-sm'
        })
    )

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError("This username is already registered.")
        return username

    def clean_registration_number(self):
        reg_num = self.cleaned_data.get('registration_number')
        if Student.objects.filter(registration_number=reg_num).exists():
            raise forms.ValidationError("This student registration number is already registered.")
        return reg_num
