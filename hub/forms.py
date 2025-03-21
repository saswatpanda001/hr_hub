from django import forms
from hub.models import UserProfile, Job, Notifications, Interview


class NotificationForm(forms.ModelForm):
    class Meta:
        model = Notifications
        fields = ['title', 'description', 'sender']


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = [
            'profile_picture', 'role', 'phone', 'address', 'city', 
            'state', 'country', 'linkedin_url', 'github_url', 'bio', 
            'date_of_birth'
        ]

class JobForm(forms.ModelForm):
    class Meta:
        model = Job
        fields = ["title", "description", "salary", "location", "status", "type", "qualifications", "skills"]
        widgets = {
            "title": forms.TextInput(attrs={"class": "border rounded-lg p-2 w-full"}),
            "description": forms.Textarea(attrs={"class": "border rounded-lg p-2 w-full", "rows": 4}),
            "salary": forms.NumberInput(attrs={"class": "border rounded-lg p-2 w-full"}),
            "location": forms.TextInput(attrs={"class": "border rounded-lg p-2 w-full"}),
            "status": forms.Select(attrs={"class": "border rounded-lg p-2 w-full"}),
            "type": forms.Select(attrs={"class": "border rounded-lg p-2 w-full"}),
            "qualifications": forms.SelectMultiple(attrs={"class": "border rounded-lg p-2 w-full"}),
            "skills": forms.SelectMultiple(attrs={"class": "border rounded-lg p-2 w-full"}),
        }


class InterviewForm(forms.ModelForm):
    class Meta:
        model = Interview
        fields = ['interview_date', 'interview_location', 'interview_notes']


