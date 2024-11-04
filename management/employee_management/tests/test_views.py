import pytest
from rest_framework.test import APIRequestFactory
from rest_framework import status
from employee_management.models.employee_model import Employee
from employee_management.views.employee_view import EmployeeView

@pytest.mark.django_db
class TestEmployeeView:
    
    def setup_method(self):
        self.factory = APIRequestFactory()

    def test_get_employee(self):
        employee = Employee.objects.create(name="John Doe", position="Developer", email="john@example.com", date_joined="2023-01-01")
        view = EmployeeView.as_view()
        request = self.factory.get(f'/employees/{employee.id}/')
        response = view(request, id=employee.id)
        assert response.status_code == status.HTTP_200_OK
        assert response.data['name'] == "John Doe"

    def test_post_employee(self):
        view = EmployeeView.as_view()
        data = {
            "name": "Jane Doe",
            "position": "Manager",
            "email": "jane@example.com",
            "date_joined": "2023-01-01"
        }
        request = self.factory.post('/employees/', data)
        response = view(request)
        assert response.status_code == status.HTTP_201_CREATED
        assert Employee.objects.filter(name="Jane Doe").exists()

    def test_put_employee(self):
        employee = Employee.objects.create(name="John Doe", position="Developer", email="john@example.com", date_joined="2023-01-01")
        view = EmployeeView.as_view()
        updated_data = {
            "name": "John Smith",
            "position": "Senior Developer"
        }
        request = self.factory.put(f'/employees/{employee.id}/', updated_data)
        response = view(request, id=employee.id)
        assert response.status_code == status.HTTP_200_OK
        employee.refresh_from_db()
        assert employee.name == "John Smith"

    def test_delete_employee(self):
        employee = Employee.objects.create(name="John Doe", position="Developer", email="john@example.com", date_joined="2023-01-01")
        view = EmployeeView.as_view()
        request = self.factory.delete(f'/employees/{employee.id}/')
        response = view(request, id=employee.id)
        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert not Employee.objects.filter(id=employee.id).exists()
