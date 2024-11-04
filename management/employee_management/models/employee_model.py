from django.db import models

class Employee(models.Model):
    name = models.CharField(max_length=100)
    position = models.CharField(max_length=100)
    department = models.CharField(
        max_length=100, 
        blank=True, 
        null=True, 
        choices=[
            ("HR", "HR"),
            ("Engineering", "Engineering"),
            ("Sales", "Sales"),
           
        ]
    )
    role = models.CharField(
        max_length=100, 
        blank=True, 
        null=True, 
        choices=[
            ("Manager", "Manager"),
            ("Developer", "Developer"),
            ("Analyst", "Analyst"),
           
        ]
    )
    email = models.EmailField(unique=True)
    date_joined = models.DateField()

    def __str__(self):
        return self.name
