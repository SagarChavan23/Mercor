from rest_framework import viewsets, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.utils import timezone
from .models import Employee, Project, Task, TimeEntry
from .serializers import EmployeeSerializer, ProjectSerializer, TaskSerializer, TimeEntrySerializer

class EmployeeViewSet(viewsets.ModelViewSet):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Employee.objects.filter(is_active=True)

    def perform_destroy(self, instance):
        instance.is_active = False
        instance.save()

class ProjectViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save()

class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save()

class TimeEntryView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, action=None):
        if action == 'start_tracking':
            if TimeEntry.objects.filter(employee=request.user, is_active=True).exists():
                return Response({'error': 'Another timer is active'}, status=status.HTTP_400_BAD_REQUEST)
            
            serializer = TimeEntrySerializer(data=request.data, context={'request': request})
            if serializer.is_valid():
                serializer.save(start_time=timezone.now())
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        elif action == 'stop_tracking':
            time_entry = TimeEntry.objects.filter(employee=request.user, is_active=True).first()
            if not time_entry:
                return Response({'error': 'No active timer'}, status=status.HTTP_400_BAD_REQUEST)
            
            time_entry.end_time = timezone.now()
            time_entry.is_active = False
            time_entry.duration_seconds = int((time_entry.end_time - time_entry.start_time).total_seconds())
            time_entry.save()
            serializer = TimeEntrySerializer(time_entry)
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        return Response({'error': 'Invalid action'}, status=status.HTTP_400_BAD_REQUEST)

class ActiveTimeEntryView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        time_entry = TimeEntry.objects.filter(employee=request.user, is_active=True).first()
        if time_entry:
            serializer = TimeEntrySerializer(time_entry)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response({}, status=status.HTTP_200_OK)
