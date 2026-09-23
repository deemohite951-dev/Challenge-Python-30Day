from django import forms
from django.contrib.auth.models import User
from .models import IssueReport

class UserRegisterForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Create password'}))
    password_confirm = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Confirm password'}))

    class Meta:
        model = User
        fields = ['username', 'email', 'password']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email Address'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        p1 = cleaned_data.get("password")
        p2 = cleaned_data.get("password_confirm")
        if p1 and p2 and p1 != p2:
            self.add_error('password_confirm', "Passwords do not match!")
        return cleaned_data

class IssueReportForm(forms.ModelForm):
    class Meta:
        model = IssueReport
        fields = ['title', 'description', 'category', 'location', 'incident_date', 'incident_time', 'photo']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'id': 'field_title', 'placeholder': 'Brief issue summary'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'id': 'field_desc', 'rows': 4, 'placeholder': 'Describe the issue...'}),
            'category': forms.Select(attrs={'class': 'form-select', 'id': 'field_category'}),
            'location': forms.TextInput(attrs={'class': 'form-control', 'id': 'field_location', 'placeholder': 'Street, landmark or area'}),
            'incident_date': forms.DateInput(attrs={'class': 'form-control', 'id': 'field_date', 'type': 'date'}),
            'incident_time': forms.TimeInput(attrs={'class': 'form-control', 'id': 'field_time', 'type': 'time'}),
            'photo': forms.FileInput(attrs={'class': 'form-control', 'id': 'field_photo', 'accept': 'image/*'}),
        }