from django.urls import path
from .views import AttendanceListView, attendance_mark, attendance_week

urlpatterns = [
    path('', AttendanceListView.as_view(), name='attendance_list'),
    path('mark/', attendance_mark, name='attendance_mark'),
    path('week/', attendance_week, name='attendance_week'),
]
