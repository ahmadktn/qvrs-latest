from django import forms
from django.contrib.auth import get_user_model
from placements.models import PlacementRequest, Placement
from organisations.models import TrainingOpportunity
from accounts.models import User

class PlacementRequestForm(forms.ModelForm):
    class Meta:
        model = PlacementRequest
        fields = ['training_opportunity', 'proposed_start_date', 'proposed_end_date', 'cover_note']
        widgets = {
            'proposed_start_date': forms.DateInput(attrs={'type': 'date', 'class': 'w-full px-4 py-2.5 rounded-lg border border-slate-300 focus:ring-2 focus:ring-blue-600 focus:border-transparent text-sm'}),
            'proposed_end_date': forms.DateInput(attrs={'type': 'date', 'class': 'w-full px-4 py-2.5 rounded-lg border border-slate-300 focus:ring-2 focus:ring-blue-600 focus:border-transparent text-sm'}),
            'cover_note': forms.Textarea(attrs={'class': 'w-full px-4 py-2.5 rounded-lg border border-slate-300 focus:ring-2 focus:ring-blue-600 focus:border-transparent text-sm', 'rows': 3, 'placeholder': 'State your SIWES goals and why you chose this organization...'}),
        }

    def __init__(self, *args, organization=None, **kwargs):
        super().__init__(*args, **kwargs)
        if organization:
            self.fields['training_opportunity'].queryset = TrainingOpportunity.objects.filter(organization=organization)
            self.fields['training_opportunity'].widget.attrs.update({'class': 'w-full px-4 py-2.5 rounded-lg border border-slate-300 focus:ring-2 focus:ring-blue-600 focus:border-transparent text-sm bg-white'})


class CoordinatorPlacementProcessForm(forms.Form):
    STATUS_CHOICES = [
        (PlacementRequest.Status.ACCEPTED, 'Accept & Approve Placement'),
        (PlacementRequest.Status.REJECTED, 'Reject Placement Request'),
    ]
    status = forms.ChoiceField(
        choices=STATUS_CHOICES,
        widget=forms.Select(attrs={'class': 'w-full px-4 py-2.5 rounded-lg border border-slate-300 focus:ring-2 focus:ring-blue-600 focus:border-transparent text-sm bg-white'})
    )
    academic_supervisor = forms.ModelChoiceField(
        queryset=User.objects.filter(role=User.Role.SUPERVISOR),
        required=False,
        help_text="Select Academic Supervisor to oversee student placement",
        widget=forms.Select(attrs={'class': 'w-full px-4 py-2.5 rounded-lg border border-slate-300 focus:ring-2 focus:ring-blue-600 focus:border-transparent text-sm bg-white'})
    )
    coordinator_feedback = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={'class': 'w-full px-4 py-2.5 rounded-lg border border-slate-300 focus:ring-2 focus:ring-blue-600 focus:border-transparent text-sm', 'rows': 2, 'placeholder': 'Optional feedback notes for student...'})
    )
