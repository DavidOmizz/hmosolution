from django.urls import path
from .views import index, documentation, register, login, logout_view, edit_hospital_profile, edit_patients_profile

urlpatterns = [
    path('home', index, name='home'),
    path('register', register, name='register'),
    path('document', documentation, name='document'),
    path('login/', login, name='login'),
    path('logout/', logout_view, name='logout'),
    path('edit-hospital-profile/', edit_hospital_profile, name='edit_hospital_profile'),
    path('edit-patients-profile/', edit_patients_profile, name = 'edit_patients_profile'),
]