from django import forms
from .models import Employee
from django.core.exceptions import ValidationError

class EmployeeForm(forms.ModelForm):
    class Meta:
        model = Employee
        fields = ['name', 'email', 'department', 'role']  # 'date_joined' is excluded since it’s auto-generated

    department = forms.CharField(
        required=False, 
        max_length=100,
        widget=forms.Select(choices=[
            ("HR", "HR"),
            ("Engineering", "Engineering"),
            ("Sales", "Sales"),
            # Add other department options as needed
        ])
    )
    
    role = forms.CharField(
        required=False, 
        max_length=100,
        widget=forms.Select(choices=[
            ("Manager", "Manager"),
            ("Developer", "Developer"),
            ("Analyst", "Analyst"),
            # Add other role options as needed
        ])
    )
    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        
        # Check for unique email within the Employee model
        if Employee.objects.filter(email=email).exists():
            raise ValidationError("An employee with this email already exists.")
        
        return email

    def save(self, commit=True):
        # Automatically set `date_joined` on creation
        employee = super().save(commit=False)
        if not employee.date_joined:
            employee.date_joined = forms.DateField().to_python(forms.fields.DateField().initial) # sets current date
        if commit:
            employee.save()
        return employee

