from django.urls import path
from worker_service import views

urlpatterns = [
    path('tasks/delete-by-pid/<int:pid>', views.DeleteTaskByPid.as_view()),
    path('tasks/update-device-task/<str:deviceId>', views.UpdateDeviceTasks.as_view())
]
