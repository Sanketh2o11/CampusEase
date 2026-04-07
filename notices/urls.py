from django.urls import path
from .views import NoticeListView, NoticeCreateView, NoticeUpdateView, NoticeDeleteView, NoticePinToggleView, poll_vote

urlpatterns = [
    path('', NoticeListView.as_view(), name='notice_list'),
    path('create/', NoticeCreateView.as_view(), name='notice_create'),
    path('<int:pk>/edit/', NoticeUpdateView.as_view(), name='notice_update'),
    path('<int:pk>/delete/', NoticeDeleteView.as_view(), name='notice_delete'),
    path('<int:pk>/pin/', NoticePinToggleView.as_view(), name='notice_pin_toggle'),
    path('<int:pk>/vote/', poll_vote, name='poll_vote'),
]
