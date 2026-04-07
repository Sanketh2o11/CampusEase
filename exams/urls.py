from django.urls import path
from .views import ExamListView, BatchExamCreateView, PersonalResultCreateView

urlpatterns = [
    path('', ExamListView.as_view(), name='exam_list'),
    path('batch/add/', BatchExamCreateView.as_view(), name='batch_exam_create'),
    path('<int:pk>/result/', PersonalResultCreateView.as_view(), name='personal_result_create'),
]
