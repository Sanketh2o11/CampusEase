from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.urls')),
    path('timetable/', include('timetable.urls')),
    path('attendance/', include('attendance.urls')),
    path('notices/', include('notices.urls')),
    path('materials/', include('materials.urls')),
    path('exams/', include('exams.urls')),
    path('lostfound/', include('lostfound.urls')),
    path('', include('core.urls')),
]
