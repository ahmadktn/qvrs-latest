from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    class Role(models.TextChoices):
        COORDINATOR = 'COORDINATOR', 'SIWES Coordinator'
        SUPERVISOR = 'SUPERVISOR', 'Academic Supervisor'
        STUDENT = 'STUDENT', 'Student'
        ORGANIZATION = 'ORGANIZATION', 'Organization Representative'

    role = models.CharField(
        max_length=20,
        choices=Role.choices,
        default=Role.STUDENT
    )
    phone_number = models.CharField(max_length=20, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    @property
    def is_coordinator(self):
        return self.role == self.Role.COORDINATOR or self.is_superuser

    @property
    def is_supervisor(self):
        return self.role == self.Role.SUPERVISOR

    @property
    def is_student(self):
        return self.role == self.Role.STUDENT

    @property
    def is_organization(self):
        return self.role == self.Role.ORGANIZATION

    def __str__(self):
        return f"{self.get_full_name() or self.username} ({self.get_role_display()})"


class Student(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='student_profile'
    )
    registration_number = models.CharField(max_length=30, unique=True)
    faculty = models.CharField(max_length=100, default='Faculty of Computing')
    department = models.CharField(max_length=100, default='Software Engineering')
    course_of_study = models.CharField(max_length=100, default='B.Sc. Software Engineering')
    level = models.CharField(max_length=10, default='400L')
    session = models.CharField(max_length=20, default='2025/2026')

    def __str__(self):
        return f"{self.registration_number} - {self.user.get_full_name() or self.user.username}"
