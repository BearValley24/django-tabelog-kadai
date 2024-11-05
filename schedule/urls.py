from django.urls import path
from . import views

app_name = "schedule"

urlpatterns = [
    path('delete/<int:pk>', views.ScheduleDelete.as_view(), name='delete'),
]