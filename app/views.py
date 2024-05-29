from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from .forms import *
from django.contrib.auth import login as auth_login, logout
from django.contrib.auth.views import PasswordResetView
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from .models import HospitalProfile




# Create your views here.

class ResetPasswordView(SuccessMessageMixin, PasswordResetView):
    template_name = 'pages/oauth/password_reset.html'
    email_template_name = 'pages/oauth/password_reset_email.html'
    subject_template_name = 'pages/oauth/password_reset_subject.txt'
    success_message = "We've emailed you instructions for setting reset your password, "\
                    "If an account exits with the email you entered. You should receive them shortly."\
                    "If you don't receive an email,"\
                    "Please make sure you've entered the address you registered with, and check your spam folder."
    success_url = reverse_lazy('login')
                        

@login_required
def index(request):
    user_type = request.user.user_type
    users = request.user
    hospitalsprofile = users
    patientsprofile = users
    context = {
        'user_type': user_type,
        'user': request.user.username,
        'hospitalprofile': hospitalsprofile,
        'patientsprofile': patientsprofile
    }
    return render(request, 'index.html', context)

def documentation(request):
    return render(request, 'documentation/documentation.html')

def register(request):
    if request.method == 'POST':
        form = RegisterationForm(request.POST)
        if form.is_valid():
            user_type = form.cleaned_data['user_type']
            user = form.save()

            if user_type == 'hospital':
                HospitalProfile.objects.create(user=user)
            elif user_type == 'patients':
                PatientsProfile.objects.create(user=user)

            messages.success(request,'Account created successfully for user %s' % user)
            return redirect('login')
        else:
            messages.error(request, form.errors)

    else:
        form = RegisterationForm()

    return render(request, 'pages/oauth/register.html', {'form': form})

def login(request):
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            auth_login(request, user)
            return redirect('/')
            # print('Okay')
        else:
            messages.warning(request, 'Username or Password is incorrect')

    else:
        form = LoginForm()
    
    return render(request, 'pages/oauth/login.html', {'form': form})

@login_required
def logout_view(request):
    logout(request)
    return redirect('login')


def edit_hospital_profile(request):
    # Ensure the user is authenticated
    if not request.user.is_authenticated:
        # Handle unauthenticated users appropriately, e.g., redirect to login page
        return redirect('login')
    try:
        hospital_profile = HospitalProfile.objects.get(user=request.user)
    except HospitalProfile.DoesNotExist:
        # Handle the case where the hospital profile does not exist for the current user
        # You may want to create a new profile or redirect to a different page
        return redirect('/')

    hospital_profile = HospitalProfile.objects.get(user=request.user)

    hospital_form = EditHospitalProfileForm(request.POST, request.FILES, instance= hospital_profile)
    if request.method == 'POST':
        hospital_form = EditHospitalProfileForm(request.POST, request.FILES, instance= hospital_profile)

        # username = self.cleaned_data['username']
        # if User.objects.exclude(pk=self.instance.user.pk).filter(username=username).exists():
        #     messages.error('User with username %s already exists')
        #     hospital_form = EditHospitalProfileForm(instance= hospital_profile)
        #     print('Username %s already exists')


        if hospital_form.is_valid():
            hospital_form.save()
            messages.success(request, 'Profile updated successfully!')
            return redirect('/')
        else:
            # Form is not valid, display errors to the user
            # You may want to render the form again with error messages
            print('Form is not valid:', hospital_form.errors)
    else:
        # messages.error(request, hospital_form.errors)
        for field, errors in hospital_form.errors.items():
                for error in errors:
                    messages.error(request, f'{field}: {error}')
        hospital_form = EditHospitalProfileForm(instance= hospital_profile)

    return render(request, 'pages/forms/edit-profile-form.html', {'form': hospital_form})

def edit_patients_profile(request):
    # Ensure the user is authenticated
    if not request.user.is_authenticated:
        # Handle unauthenticated users appropriately, e.g., redirect to login page
        return redirect('login')

    try:
        patient_profile = PatientsProfile.objects.get(user=request.user)
    except PatientsProfile.DoesNotExist:
        # Handle the case where the hospital profile does not exist for the current user
        # You may want to create a new profile or redirect to a different page
        return redirect('/')

    patient_profile = PatientsProfile.objects.get(user=request.user)

    patient_form = EditPatientProfileForm(request.POST, request.FILES, instance= patient_profile)
    if request.method == 'POST':
        patient_form = EditPatientProfileForm(request.POST, request.FILES, instance= patient_profile)

        if patient_form.is_valid():
            patient_form.save()
            messages.success(request, 'Profile updated successfully!')
            return redirect('/')
        else:
            # Form is not valid, display errors to the user
            # You may want to render the form again with error messages
            print('Form is not valid:', patient_form.errors)
    else:
        for field, errors in patient_form.errors.items():
                for error in errors:
                    messages.error(request, f'{field}: {error}')
        patient_form = EditPatientProfileForm(instance= patient_profile)

    return render(request, 'pages/forms/edit-profile-form.html', {'form': patient_form})



# def edit_hospital_profile(request):
#     # Retrieve the HospitalProfile instance associated with the current user
#     hospital_profile = HospitalProfile.objects.get(user=request.user)

#     hospital_profile = request.user.

#     if request.method == 'POST':
#         # Populate the form with POST data and files, instance with the hospital_profile
#         form = EditHospitalProfileForm(request.POST, request.FILES, instance=hospital_profile)
#         if form.is_valid():
#             # Save the form
#             form.save()
#             return redirect('profile')  # Redirect to the profile page after successful edit
#     else:
#         # If it's a GET request, populate the form with data from the hospital_profile instance
#         form = EditHospitalProfileForm(instance=hospital_profile)
    
#     return render(request, 'edit_hospital_profile.html', {'form': form})


# def edit_hospital_profile(request):
#     try:
#         # Retrieve the HospitalProfile instance associated with the current user
#         hospital_profile = HospitalProfile.objects.get(user=request.user)
#     except HospitalProfile.DoesNotExist:
#         # If no HospitalProfile exists, create a new one
#         hospital_profile = HospitalProfile.objects.create(user=request.user)
    
#     if request.method == 'POST':
#         # Populate the form with POST data and files, instance with the hospital_profile
#         form = EditHospitalProfileForm(request.POST, request.FILES, instance=hospital_profile)
#         if form.is_valid():
#             # Save the form
#             form.save()
#             return redirect('home')  # Redirect to the index page after successful edit
#     else:
#         # If it's a GET request, populate the form with data from the hospital_profile instance
#         form = EditHospitalProfileForm(instance=hospital_profile)
    
#     return render(request, 'pages/forms/edit-hospital-profile.html', {'form': form})

# def edit_hospital_profile(request):
#     try:
#         # Retrieve the HospitalProfile instance associated with the current user
#         hospital_profile = HospitalProfile.objects.get(user=request.user)
#     except HospitalProfile.DoesNotExist:
#         # If no HospitalProfile exists, create a new one
#         hospital_profile = HospitalProfile.objects.create(user=request.user)
    
#     if request.method == 'POST':
#         # Populate the form with POST data and files, instance with the hospital_profile
#         form = EditHospitalProfileForm(request.POST, request.FILES, instance=hospital_profile)
#         if form.is_valid():
#             print("Form is valid")  # Debug print
#             # Save the form
#             form.save()
#             print("Form saved successfully")  # Debug print
#             return redirect('home')  # Redirect to the index page after successful edit
#         else:
#             print("Form errors:", form.errors)  # Debug print
#     else:
#         # If it's a GET request, populate the form with data from the hospital_profile instance
#         form = EditHospitalProfileForm(instance=hospital_profile)
    
#     return render(request, 'pages/forms/edit-hospital-profile.html', {'form': form})


# def edit_patients_profile(request):
#     # Retrieve the HospitalProfile instance associated with the current user
#     patients_profile = PatientsProfile.objects.get(user=request.user)

#     if request.method == 'POST':
#         # Populate the form with POST data and files, instance with the hospital_profile
#         form = EditPatientProfileForm(request.POST, request.FILES, instance=patients_profile)
#         if form.is_valid():
#             # Save the form
#             form.save()
#             return redirect('profile')  # Redirect to the profile page after successful edit
#     else:
#         # If it's a GET request, populate the form with data from the hospital_profile instance
#         form = EditHospitalProfileForm(instance=patients_profile)
    
#     return render(request, 'edit_patients_profile.html', {'form': form})