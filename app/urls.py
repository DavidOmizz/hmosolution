from django.urls import path
from .views import index, documentation, register, login, logout_view, edit_hospital_profile, edit_patients_profile, ResetPasswordView
from django.contrib.auth import views as auth_views
urlpatterns = [
    path('', index, name='home'),
    path('register', register, name='register'),
    path('document', documentation, name='document'),
    path('login/', login, name='login'),
    path('logout/', logout_view, name='logout'),
    path('edit-hospital-profile/', edit_hospital_profile, name='edit_hospital_profile'),
    path('edit-patients-profile/', edit_patients_profile, name = 'edit_patients_profile'),
    path('password-reset/', ResetPasswordView.as_view(), name='password_reset'),
    path('password-reset-confirm/<uidb64>/<token>/',
        auth_views.PasswordResetConfirmView.as_view(template_name='pages/oauth/password_reset_confirm.html'),
        name='password_reset_confirm'),
    path('password-reset-complete/',
         auth_views.PasswordResetCompleteView.as_view(template_name='pages/oauth/password_reset_complete.html'),
         name='password_reset_complete'),
]