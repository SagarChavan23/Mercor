from django.db import models
from django.contrib.auth.models import AbstractUser
import uuid

class Employee(AbstractUser):
    employee_id = models.CharField(max_length=50, unique=True, blank=True, null=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.username

class Project(models.Model):
    id = models.CharField(max_length=50, primary_key=True, default=uuid.uuid4)
    name = models.CharField(max_length=100)
    employees = models.ManyToManyField(Employee, related_name='projects')

    def __str__(self):
        return self.name

class Task(models.Model):
    id = models.CharField(max_length=50, primary_key=True, default=uuid.uuid4)
    name = models.CharField(max_length=100)
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='tasks')
    employees = models.ManyToManyField(Employee, related_name='tasks')

    def __str__(self):
        return f"{self.project.name} - {self.name}"

class TimeEntry(models.Model):
    id = models.CharField(max_length=50, primary_key=True, default=uuid.uuid4)
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='time_entries')
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    task_name = models.CharField(max_length=100)
    project_name = models.CharField(max_length=100)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField(null=True, blank=True)
    duration_seconds = models.IntegerField(null=True, blank=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.employee.username} - {self.task_name} ({self.start_time})"
