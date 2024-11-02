from django import forms
import re

class EmployeeForm(forms.Form):
    name = forms.CharField(required=True, min_length=1, max_length=255)
    email = forms.EmailField(required=True)
    department = forms.CharField(required=False, max_length=100)
    role = forms.CharField(required=False, max_length=100)
    date_joined = forms.DateField(required=False)

    def clean_email(self):
        email = self.cleaned_data.get('email')
        
        # Custom email validation can be added here if necessary
        if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
            self.add_error('email', 'Enter a valid email address.')
        
        return email

    def clean(self):
        cleaned_data = super().clean()
        
        # Additional validation can be added here if needed for other fields
        return cleaned_data
