from django.urls import path
from .views import (
    LostFoundIndexView, LostFoundResolveView, LostFoundDeleteView,
    LostFoundFoundView, LostFoundClaimView,
)

urlpatterns = [
    path('', LostFoundIndexView.as_view(), name='lostfound_list'),
    path('<int:pk>/resolve/', LostFoundResolveView.as_view(), name='lostfound_resolve'),
    path('<int:pk>/found/', LostFoundFoundView.as_view(), name='lostfound_found'),
    path('<int:pk>/claim/', LostFoundClaimView.as_view(), name='lostfound_claim'),
    path('<int:pk>/delete/', LostFoundDeleteView.as_view(), name='lostfound_delete'),
]
