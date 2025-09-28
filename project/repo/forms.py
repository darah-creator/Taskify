from django import forms
from .models import Tasks
from django.contrib.auth.models import User


class SubmissionForm(forms.ModelForm):
    class Meta:
        model = Tasks
        fields = ["file"]


class TaskForm(forms.ModelForm):
    assign_to = forms.ModelMultipleChoiceField(
        queryset=User.objects.all(),
        required=False,
        widget=forms.CheckboxSelectMultiple,
        label="Assign to"
    )
    assign_all = forms.BooleanField(
        required=False,
        label="Assign to all users"
    )

    class Meta:
        model = Tasks
        fields = ["title", "description", "assign_to", "assign_all"]