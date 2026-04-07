from django import forms
from .models import BatchExam, PersonalExamResult


class BatchExamForm(forms.ModelForm):
    class Meta:
        model = BatchExam
        fields = ['subject', 'exam_name', 'exam_type', 'exam_date', 'syllabus']
        widgets = {
            'exam_date': forms.DateInput(attrs={'type': 'date'}),
            'syllabus': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Syllabus covered (optional)'}),
        }


class PersonalExamResultForm(forms.ModelForm):
    class Meta:
        model = PersonalExamResult
        fields = ['score', 'notes']
        widgets = {
            'notes': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Personal notes about your performance...'}),
        }
