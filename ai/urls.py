from django.urls import path
from .views import AIAssistView

urlpatterns = [
    path('assist/', AIAssistView.as_view(), name='ai_assist'),
]
