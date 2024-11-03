from django.urls import path
from . import views

app_name = "schedule"

urlpatterns = [
    path('calendar/', views.Calendar.as_view(), name='calendar'),
    #path('calendar/<int:year>/<int:month>/<int:day>/', views.Calendar.as_view(), name='calendar'),
    #path('calendar/<int:pk>/', views.Calendar.as_view(), name='calendar'),
    #path('calendar/<int:year>/<int:month>/<int:day>/', views.Calendar_original.as_view(), name='calendar'),
    path('calendar/<int:year>/<int:month>/<int:day>/<str:input_data>/', views.Calendar2.as_view(), name='calendar2'),
    path('booking/<int:year>/<int:month>/<int:day>/', views.Booking.as_view(), name='booking'),
    #path('booking/', views.Booking.as_view(), name='booking'),
    path('delete/<int:pk>', views.ScheduleDelete.as_view(), name='delete'),

]