from django.urls import path
from . import views
from .views import add_patient, submit_lab_result, success_view

urlpatterns = [
    path('', views.add_patient, name='add_patient'),
    path('submit_lab_result/<str:outpatient_number>/', submit_lab_result, name='submit_lab_result'),
    path('success/', views.success_view, name='success'),  # Define a success page
    #path('<int:patient_id>/', views.patient_detail, name='patient_detail'),
]
