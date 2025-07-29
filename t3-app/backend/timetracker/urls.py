from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from . import views

router = DefaultRouter()
router.register(r'employees', views.EmployeeViewSet, basename='employee')
router.register(r'projects', views.ProjectViewSet, basename='project')
router.register(r'tasks', views.TaskViewSet, basename='task')

urlpatterns = [
    path('api/', include(router.urls)),
    path('api/login/', TokenObtainPairView.as_view(), name='login'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/time-entries/start_tracking/', views.TimeEntryView.as_view(), {'action': 'start_tracking'}, name='start_tracking'),
    path('api/time-entries/stop_tracking/', views.TimeEntryView.as_view(), {'action': 'stop_tracking'}, name='stop_tracking'),
    path('api/time-entries/active/', views.ActiveTimeEntryView.as_view(), name='active_time_entry'),
]
