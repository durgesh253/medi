from django.urls import path
from .views import *

urlpatterns = [
    path("",login_view, name="login_view"),
    path("indexpage/", IndexPage, name="indexpage"),
    path("forgot-password/",forgot_password, name="forgot_password"),
    path("otp_verification",otp_verification, name="otp_verification"),
    path('logout/',logout, name="logout"),
    path('update_profile/<str:staff_id>', update_profile, name='update_profile'),
    path("dashboard_view/",dashboard_view, name="dashboard_view"),
    path("doctors_view",doctor_view, name="doctors_view"),
    path('create_doctor/', create_doctor, name='create_doctor'),
    path("add_patient/",add_patient,name="add_patient"),
    path('update_patient/<int:patient_id>/', update_patient, name='update_patient'),
    path("delete_patient/<int:patient_id>",delete_patient,name="delete_patient"),
    path("patient_list/",patient_list,name="patient_list"),
]
