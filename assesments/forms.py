from django import forms
from assesments.models import SupervisorAssessment, OrganizationReview, BlacklistRecord

class SupervisorAssessmentForm(forms.ModelForm):
    class Meta:
        model = SupervisorAssessment
        fields = [
            'q1_skill_relevance',
            'q2_supervision_adequacy',
            'q3_curriculum_alignment',
            'q4_recommend_future',
            'observed_student_tasks',
            'qualitative_feedback'
        ]
        widgets = {
            'q1_skill_relevance': forms.Select(attrs={'class': 'w-full px-4 py-2.5 rounded-lg border border-slate-300 focus:ring-2 focus:ring-blue-600 focus:border-transparent text-sm bg-white'}),
            'q2_supervision_adequacy': forms.Select(attrs={'class': 'w-full px-4 py-2.5 rounded-lg border border-slate-300 focus:ring-2 focus:ring-blue-600 focus:border-transparent text-sm bg-white'}),
            'q3_curriculum_alignment': forms.Select(attrs={'class': 'w-full px-4 py-2.5 rounded-lg border border-slate-300 focus:ring-2 focus:ring-blue-600 focus:border-transparent text-sm bg-white'}),
            'q4_recommend_future': forms.Select(attrs={'class': 'w-full px-4 py-2.5 rounded-lg border border-slate-300 focus:ring-2 focus:ring-blue-600 focus:border-transparent text-sm bg-white'}),
            'observed_student_tasks': forms.Textarea(attrs={'class': 'w-full px-4 py-2.5 rounded-lg border border-slate-300 focus:ring-2 focus:ring-blue-600 focus:border-transparent text-sm', 'rows': 3, 'placeholder': 'Detail the concrete technical projects and tasks the student actually performed...'}),
            'qualitative_feedback': forms.Textarea(attrs={'class': 'w-full px-4 py-2.5 rounded-lg border border-slate-300 focus:ring-2 focus:ring-blue-600 focus:border-transparent text-sm', 'rows': 4, 'placeholder': 'General assessment narrative on organization commitment, facilities, mentorship quality, and curriculum alignment...'}),
        }


class DepartmentalReviewForm(forms.ModelForm):
    class Meta:
        model = OrganizationReview
        fields = ['outcome', 'review_notes']
        widgets = {
            'outcome': forms.Select(attrs={'class': 'w-full px-4 py-2.5 rounded-lg border border-slate-300 focus:ring-2 focus:ring-blue-600 focus:border-transparent text-sm bg-white'}),
            'review_notes': forms.Textarea(attrs={'class': 'w-full px-4 py-2.5 rounded-lg border border-slate-300 focus:ring-2 focus:ring-blue-600 focus:border-transparent text-sm', 'rows': 4, 'placeholder': 'Document committee hearing notes, formal rationale, and review decisions...'}),
        }


class BlacklistActionForm(forms.Form):
    reason = forms.CharField(
        widget=forms.Textarea(attrs={'class': 'w-full px-4 py-2.5 rounded-lg border border-slate-300 focus:ring-2 focus:ring-blue-600 focus:border-transparent text-sm', 'rows': 4, 'placeholder': 'State formal departmental reason for blacklisting this organization...'})
    )
