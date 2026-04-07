from django.urls import path
from .views import MaterialListView, MaterialCreateView, MaterialDeleteView, MaterialPinToggleView, material_thankyou

urlpatterns = [
    path('', MaterialListView.as_view(), name='material_list'),
    path('upload/', MaterialCreateView.as_view(), name='material_upload'),
    path('<int:pk>/delete/', MaterialDeleteView.as_view(), name='material_delete'),
    path('<int:pk>/pin/', MaterialPinToggleView.as_view(), name='material_pin_toggle'),
    path('<int:pk>/thankyou/', material_thankyou, name='material_thankyou'),
]
