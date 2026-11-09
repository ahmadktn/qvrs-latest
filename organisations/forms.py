from django import forms
from organisations.models import Organization, TrainingOpportunity, OrganizationVetting

class OrganizationSubmissionForm(forms.ModelForm):
    class Meta:
        model = Organization
        fields = [
            'name', 'registration_number', 'industry_sector',
            'services_provided', 'address', 'city', 'local_government', 'state',
            'website', 'contact_person_name', 'contact_person_email',
            'contact_person_phone'
        ]
        widgets = {
            'name': forms.TextInput(attrs={'class': 'w-full px-4 py-2.5 rounded-lg border border-slate-300 focus:ring-2 focus:ring-blue-600 focus:border-transparent text-sm', 'placeholder': 'e.g., Kano Tech Hub Ltd'}),
            'registration_number': forms.TextInput(attrs={'class': 'w-full px-4 py-2.5 rounded-lg border border-slate-300 focus:ring-2 focus:ring-blue-600 focus:border-transparent text-sm', 'placeholder': 'CAC RC-123456'}),
            'industry_sector': forms.TextInput(attrs={'class': 'w-full px-4 py-2.5 rounded-lg border border-slate-300 focus:ring-2 focus:ring-blue-600 focus:border-transparent text-sm', 'placeholder': 'e.g., Software Engineering, FinTech, Telecom'}),
            'services_provided': forms.Textarea(attrs={'class': 'w-full px-4 py-2.5 rounded-lg border border-slate-300 focus:ring-2 focus:ring-blue-600 focus:border-transparent text-sm', 'rows': 3, 'placeholder': 'Describe core business operations and technical products...'}),
            'address': forms.Textarea(attrs={'class': 'w-full px-4 py-2.5 rounded-lg border border-slate-300 focus:ring-2 focus:ring-blue-600 focus:border-transparent text-sm', 'rows': 2, 'placeholder': 'Physical office address...'}),
            'city': forms.TextInput(attrs={'class': 'w-full px-4 py-2.5 rounded-lg border border-slate-300 focus:ring-2 focus:ring-blue-600 focus:border-transparent text-sm'}),
            'local_government': forms.TextInput(attrs={'class': 'w-full px-4 py-2.5 rounded-lg border border-slate-300 focus:ring-2 focus:ring-blue-600 focus:border-transparent text-sm', 'placeholder': 'e.g., Kano Municipal, Nassarawa, Gwale'}),
            'state': forms.TextInput(attrs={'class': 'w-full px-4 py-2.5 rounded-lg border border-slate-300 focus:ring-2 focus:ring-blue-600 focus:border-transparent text-sm'}),
            'website': forms.URLInput(attrs={'class': 'w-full px-4 py-2.5 rounded-lg border border-slate-300 focus:ring-2 focus:ring-blue-600 focus:border-transparent text-sm', 'placeholder': 'https://example.com'}),
            'contact_person_name': forms.TextInput(attrs={'class': 'w-full px-4 py-2.5 rounded-lg border border-slate-300 focus:ring-2 focus:ring-blue-600 focus:border-transparent text-sm'}),
            'contact_person_email': forms.EmailInput(attrs={'class': 'w-full px-4 py-2.5 rounded-lg border border-slate-300 focus:ring-2 focus:ring-blue-600 focus:border-transparent text-sm'}),
            'contact_person_phone': forms.TextInput(attrs={'class': 'w-full px-4 py-2.5 rounded-lg border border-slate-300 focus:ring-2 focus:ring-blue-600 focus:border-transparent text-sm'}),
        }

    def clean_name(self):
        name = self.cleaned_data.get('name', '').strip()
        if Organization.objects.filter(name__iexact=name).exists():
            raise forms.ValidationError(f"The organization '{name}' is already registered in the system. Re-registration is not allowed.")
        return name

    def clean_local_government(self):
        lg = self.cleaned_data.get('local_government', '').strip()
        if not lg:
            raise forms.ValidationError("Local government is required.")
        return lg

    def clean_registration_number(self):
        rc = self.cleaned_data.get('registration_number', '').strip()
        if rc and Organization.objects.filter(registration_number__iexact=rc).exists():
            raise forms.ValidationError(f"An organization with CAC RC number '{rc}' is already registered in the system.")
        return rc


class TrainingOpportunityForm(forms.ModelForm):
    class Meta:
        model = TrainingOpportunity
        fields = ['role_title', 'role_description', 'expected_skills', 'curriculum_relevance_notes']
        widgets = {
            'role_title': forms.TextInput(attrs={'class': 'w-full px-4 py-2.5 rounded-lg border border-slate-300 focus:ring-2 focus:ring-blue-600 focus:border-transparent text-sm', 'placeholder': 'e.g., Junior Software Engineering Intern'}),
            'role_description': forms.Textarea(attrs={'class': 'w-full px-4 py-2.5 rounded-lg border border-slate-300 focus:ring-2 focus:ring-blue-600 focus:border-transparent text-sm', 'rows': 3, 'placeholder': 'Specific day-to-day software engineering tasks (photocopying or menial tasks are rejected)...'}),
            'expected_skills': forms.Textarea(attrs={'class': 'w-full px-4 py-2.5 rounded-lg border border-slate-300 focus:ring-2 focus:ring-blue-600 focus:border-transparent text-sm', 'rows': 2, 'placeholder': 'e.g., Python, Django, Git, REST APIs, PostgreSQL'}),
            'curriculum_relevance_notes': forms.Textarea(attrs={'class': 'w-full px-4 py-2.5 rounded-lg border border-slate-300 focus:ring-2 focus:ring-blue-600 focus:border-transparent text-sm', 'rows': 2, 'placeholder': 'How this role aligns with B.Sc. Software Engineering curriculum...'}),
        }


class OrganizationVettingForm(forms.ModelForm):
    class Meta:
        model = OrganizationVetting
        fields = [
            'decision', 'core_business_match_score', 'training_role_suitability_score',
            'capacity_assessment', 'coordinator_comments'
        ]
        widgets = {
            'decision': forms.Select(attrs={'class': 'w-full px-4 py-2.5 rounded-lg border border-slate-300 focus:ring-2 focus:ring-blue-600 focus:border-transparent text-sm bg-white'}),
            'core_business_match_score': forms.Select(attrs={'class': 'w-full px-4 py-2.5 rounded-lg border border-slate-300 focus:ring-2 focus:ring-blue-600 focus:border-transparent text-sm bg-white'}),
            'training_role_suitability_score': forms.Select(attrs={'class': 'w-full px-4 py-2.5 rounded-lg border border-slate-300 focus:ring-2 focus:ring-blue-600 focus:border-transparent text-sm bg-white'}),
            'capacity_assessment': forms.Textarea(attrs={'class': 'w-full px-4 py-2.5 rounded-lg border border-slate-300 focus:ring-2 focus:ring-blue-600 focus:border-transparent text-sm', 'rows': 3, 'placeholder': 'Assess technical facilities, mentorship quality, and office environment...'}),
            'coordinator_comments': forms.Textarea(attrs={'class': 'w-full px-4 py-2.5 rounded-lg border border-slate-300 focus:ring-2 focus:ring-blue-600 focus:border-transparent text-sm', 'rows': 3, 'placeholder': 'Mandatory detailed comments justifying decision...'}),
        }
