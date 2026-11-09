from django import forms
from django.contrib.auth import get_user_model
from accounts.models import Student

User = get_user_model()

NIGERIAN_STATES = [
    ('', '-- Select State --'),
    ('Abia', 'Abia'),
    ('Adamawa', 'Adamawa'),
    ('Akwa Ibom', 'Akwa Ibom'),
    ('Anambra', 'Anambra'),
    ('Bauchi', 'Bauchi'),
    ('Bayelsa', 'Bayelsa'),
    ('Benue', 'Benue'),
    ('Borno', 'Borno'),
    ('Cross River', 'Cross River'),
    ('Delta', 'Delta'),
    ('Ebonyi', 'Ebonyi'),
    ('Edo', 'Edo'),
    ('Ekiti', 'Ekiti'),
    ('Enugu', 'Enugu'),
    ('FCT - Abuja', 'FCT - Abuja'),
    ('Gombe', 'Gombe'),
    ('Imo', 'Imo'),
    ('Jigawa', 'Jigawa'),
    ('Kaduna', 'Kaduna'),
    ('Kano', 'Kano'),
    ('Katsina', 'Katsina'),
    ('Kebbi', 'Kebbi'),
    ('Kogi', 'Kogi'),
    ('Kwara', 'Kwara'),
    ('Lagos', 'Lagos'),
    ('Nasarawa', 'Nasarawa'),
    ('Niger', 'Niger'),
    ('Ogun', 'Ogun'),
    ('Ondo', 'Ondo'),
    ('Osun', 'Osun'),
    ('Oyo', 'Oyo'),
    ('Plateau', 'Plateau'),
    ('Rivers', 'Rivers'),
    ('Sokoto', 'Sokoto'),
    ('Taraba', 'Taraba'),
    ('Yobe', 'Yobe'),
    ('Zamfara', 'Zamfara'),
]


class LoginForm(forms.Form):
    login_id = forms.CharField(
        label='Email Address / Reg Number',
        widget=forms.TextInput(attrs={
            'class': 'w-full px-4 py-2.5 rounded-lg border border-slate-300 focus:ring-2 focus:ring-blue-600 focus:border-transparent text-slate-800 text-sm placeholder-slate-400',
            'placeholder': 'Enter your email address or registration number',
            'id': 'id_login_id'
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
    full_name = forms.CharField(
        label='Full Name',
        max_length=255,
        widget=forms.TextInput(attrs={
            'class': 'w-full px-4 py-2.5 rounded-lg border border-slate-300 focus:ring-2 focus:ring-blue-600 focus:border-transparent text-slate-800 text-sm',
            'placeholder': 'e.g. Fatima Mohammed Aliyu'
        })
    )
    registration_number = forms.CharField(
        label='BUK Registration Number',
        max_length=30,
        widget=forms.TextInput(attrs={
            'class': 'w-full px-4 py-2.5 rounded-lg border border-slate-300 focus:ring-2 focus:ring-blue-600 focus:border-transparent text-slate-800 text-sm uppercase',
            'placeholder': 'CST/20/SWE/00123'
        })
    )
    email = forms.EmailField(
        label='Email',
        widget=forms.EmailInput(attrs={
            'class': 'w-full px-4 py-2.5 rounded-lg border border-slate-300 focus:ring-2 focus:ring-blue-600 focus:border-transparent text-slate-800 text-sm',
            'placeholder': 'student@student.buk.edu.ng'
        })
    )
    faculty = forms.CharField(
        label='Faculty',
        initial='Faculty of Computing',
        required=False,
        widget=forms.TextInput(attrs={
            'readonly': 'readonly',
            'class': 'w-full px-4 py-2.5 rounded-lg border border-slate-200 bg-slate-100 text-slate-500 text-sm cursor-not-allowed select-none'
        })
    )
    department = forms.CharField(
        label='Department',
        initial='Software Engineering',
        required=False,
        widget=forms.TextInput(attrs={
            'readonly': 'readonly',
            'class': 'w-full px-4 py-2.5 rounded-lg border border-slate-200 bg-slate-100 text-slate-500 text-sm cursor-not-allowed select-none'
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

    def clean_registration_number(self):
        reg_num = self.cleaned_data.get('registration_number', '').strip()
        if Student.objects.filter(registration_number__iexact=reg_num).exists():
            raise forms.ValidationError("This registration number is already registered in the system.")
        if User.objects.filter(username__iexact=reg_num).exists():
            raise forms.ValidationError("An account with this registration number already exists.")
        return reg_num

    def clean_email(self):
        email = self.cleaned_data.get('email', '').strip().lower()
        if User.objects.filter(email__iexact=email).exists():
            raise forms.ValidationError("An account with this email address is already registered.")
        return email

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password and confirm_password and password != confirm_password:
            self.add_error('confirm_password', "Passwords do not match. Please enter the same password in both fields.")
        return cleaned_data


class SupervisorCreationForm(forms.Form):
    full_name = forms.CharField(
        label='Full Name',
        max_length=255,
        widget=forms.TextInput(attrs={
            'class': 'w-full px-4 py-2.5 rounded-lg border border-slate-300 focus:ring-2 focus:ring-blue-600 focus:border-transparent text-slate-800 text-sm',
            'placeholder': 'e.g. Dr. Usman Suleiman'
        })
    )
    email = forms.EmailField(
        label='Email',
        widget=forms.EmailInput(attrs={
            'class': 'w-full px-4 py-2.5 rounded-lg border border-slate-300 focus:ring-2 focus:ring-blue-600 focus:border-transparent text-slate-800 text-sm',
            'placeholder': 'usman.swe@buk.edu.ng'
        })
    )
    state = forms.ChoiceField(
        label='Assigned Supervision State',
        choices=NIGERIAN_STATES,
        help_text='State where supervisor conducts SIWES host organization inspections',
        widget=forms.Select(attrs={
            'class': 'w-full px-4 py-2.5 rounded-lg border border-slate-300 focus:ring-2 focus:ring-blue-600 focus:border-transparent text-slate-800 text-sm bg-white'
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

    def clean_email(self):
        email = self.cleaned_data.get('email', '').strip().lower()
        if User.objects.filter(email__iexact=email).exists():
            raise forms.ValidationError("A user with this email address already exists.")
        if User.objects.filter(username__iexact=email).exists():
            raise forms.ValidationError("A user with this username/email already exists.")
        return email

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password and confirm_password and password != confirm_password:
            self.add_error('confirm_password', "Passwords do not match.")
        return cleaned_data
