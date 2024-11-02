# serializers.py
from rest_framework import serializers
from employee_management.models.employee_model import Employee

class EmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = ['id', 'name', 'position', 'department', 'email', 'hire_date']
