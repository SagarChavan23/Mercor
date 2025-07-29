from rest_framework import serializers
from .models import Employee, Project, Task, TimeEntry
import uuid

class EmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = ['id', 'username', 'employee_id', 'is_active']

    def create(self, validated_data):
        employee = Employee.objects.create_user(
            username=validated_data['username'],
            password=validated_data.get('password', 'defaultpass'),
            employee_id=validated_data.get('employee_id', str(uuid.uuid4())),
            is_active=validated_data.get('is_active', True)
        )
        return employee

class ProjectSerializer(serializers.ModelSerializer):
    employee_ids = serializers.ListField(
        child=serializers.CharField(), write_only=True, required=False
    )

    class Meta:
        model = Project
        fields = ['id', 'name', 'employee_ids']

    def create(self, validated_data):
        employee_ids = validated_data.pop('employee_ids', [])
        project = Project.objects.create(**validated_data)
        if employee_ids:
            employees = Employee.objects.filter(id__in=employee_ids, is_active=True)
            project.employees.set(employees)
        return project

    def update(self, instance, validated_data):
        employee_ids = validated_data.pop('employee_ids', None)
        instance.name = validated_data.get('name', instance.name)
        instance.save()
        if employee_ids is not None:
            employees = Employee.objects.filter(id__in=employee_ids, is_active=True)
            instance.employees.set(employees)
        return instance

class TaskSerializer(serializers.ModelSerializer):
    project_id = serializers.CharField(write_only=True)
    employee_ids = serializers.ListField(
        child=serializers.CharField(), write_only=True, required=False
    )

    class Meta:
        model = Task
        fields = ['id', 'name', 'project_id', 'employee_ids']

    def create(self, validated_data):
        project_id = validated_data.pop('project_id')
        employee_ids = validated_data.pop('employee_ids', [])
        try:
            project = Project.objects.get(id=project_id)
        except Project.DoesNotExist:
            raise serializers.ValidationError("Project not found")
        task = Task.objects.create(project=project, **validated_data)
        if employee_ids:
            employees = Employee.objects.filter(id__in=employee_ids, is_active=True)
            task.employees.set(employees)
        return task

class TimeEntrySerializer(serializers.ModelSerializer):
    task_id = serializers.CharField(write_only=True)

    class Meta:
        model = TimeEntry
        fields = ['id', 'task_id', 'task_name', 'project_name', 'start_time', 'end_time', 'duration_seconds', 'is_active']
        read_only_fields = ['task_name', 'project_name', 'duration_seconds', 'is_active']

    def create(self, validated_data):
        task_id = validated_data.pop('task_id')
        try:
            task = Task.objects.get(id=task_id)
        except Task.DoesNotExist:
            raise serializers.ValidationError("Task not found")
        validated_data['task'] = task
        validated_data['task_name'] = task.name
        validated_data['project_name'] = task.project.name
        validated_data['employee'] = self.context['request'].user
        return TimeEntry.objects.create(**validated_data)
