from django.urls import path
from .views import TimetableStudentView, TimetableEditView

urlpatterns = [
    path('', TimetableStudentView.as_view(), name='timetable_view'),
    path('edit/', TimetableEditView.as_view(), name='timetable_edit'),
]
