# urls.py
from django.urls import path
from employee_management.views.employee_view import EmployeeView
# .employee_management.views import employee_view

urlpatterns = [
    path('employees/', EmployeeView.as_view()),          # For list and create
    path('employees/<int:id>/', EmployeeView.as_view()), # For retrieve, update, delete
]
