from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from employee_management.models.employee_model import Employee
from employee_management.serializers import EmployeeSerializer
from django.http import JsonResponse
from django.db import IntegrityError, OperationalError
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from rest_framework.exceptions import ValidationError
class EmployeeView(APIView):
    
    def get(self, request, id=None):
        authentication_classes = [TokenAuthentication]
        permission_classes = [IsAuthenticated]

        """Retrieve a single employee by ID or list all employees."""
        try:
            if id:
                employee = get_object_or_404(Employee, id=id)
                serializer = EmployeeSerializer(employee)
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                employees = Employee.objects.all()
                serializer = EmployeeSerializer(employees, many=True)
                return Response(serializer.data, status=status.HTTP_200_OK)
        except OperationalError as e:
            return Response({"detail": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
    def post(self, request):
        """Create a new employee and generate an authentication token."""
        # Create a serializer instance with the incoming data
        
        if 'password' not in request.data or not request.data['password']:
            raise ValidationError({"password": "Password is required."})
        serializer = EmployeeSerializer(data=request.data)
        
        if serializer.is_valid():
            # Save the employee object
            employee = serializer.save()
            
            # Create a user associated with this employee
            user = User.objects.create_user(
                username=request.data['email'],  # Using email as username for uniqueness
                password=request.data['password'],  # Use the provided password
                email=request.data['email']  # Ensure the email is included
            )
            
            # Create a token for the new user
            token = Token.objects.create(user=user)
            
            return Response({
                "employee": serializer.data,
                "token": token.key  # Return the token in the response
            }, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    # def post(self, request):
    #     """Create a new employee."""
    #     try:
    #         serializer = EmployeeSerializer(data=request.data)
    #         if serializer.is_valid():
    #             serializer.save()
    #             return Response(serializer.data, status=status.HTTP_201_CREATED)
    #         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    #     except IntegrityError as e:
    #         return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)
    #     except Exception as e:
    #         return Response({"detail": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def put(self, request, id=None):
        authentication_classes = [TokenAuthentication]
        permission_classes = [IsAuthenticated]
        """Update an existing employee by ID."""
        try:
            employee = get_object_or_404(Employee, id=id)
            serializer = EmployeeSerializer(employee, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except IntegrityError as e:
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"detail": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def delete(self, request, id=None):
        authentication_classes = [TokenAuthentication]
        permission_classes = [IsAuthenticated]
        """Delete an employee by ID."""
        try:
            employee = get_object_or_404(Employee, id=id)
            employee.delete()
            return JsonResponse({
                "message": "Employee deleted successfully",
                "data": {"id": id}
            }, status=status.HTTP_204_NO_CONTENT)
        except OperationalError as e:
            return Response({"detail": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        except Exception as e:
            return Response({"detail": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
