from django import forms

from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, UserChangeForm
from .models import *
from django.contrib import messages


class RegisterationForm(UserCreationForm):
    username = forms.CharField(required=True, label='Username', widget=forms.TextInput(attrs={'placeholder': 'Username', 'class': 'form-control'}))
    email = forms.EmailField(required=True, label='Email', widget=forms.TextInput(attrs={'placeholder': 'Email', 'class': 'form-control'}))
    password1 = forms.CharField(required=True, label='Password', widget=forms.PasswordInput(attrs={'placeholder': 'Password', 'class': 'form-control'}))
    password2 = forms.CharField(required=True, label='Password', widget=forms.PasswordInput(attrs={'placeholder': 'Confirm Password', 'class': 'form-control'}))
    user_type = forms.ChoiceField(required=True,label='User Type',choices=User.USER_TYPE[1:3],widget=forms.Select(attrs={'placeholder': 'Select', 'class': 'form-control'}))
    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2', 'user_type')


class LoginForm(AuthenticationForm):
    username = forms.CharField(required=True, label = 'username', widget= forms.TextInput(attrs={'placeholder':'Username', 'class': 'form-control'}))
    password = forms.CharField(
        required=True,
        label='Password',
        widget=forms.PasswordInput(attrs={'placeholder': 'Password', 'class': 'form-control'})
    )

# class EditHospitalProfileForm(UserChangeForm):
#     class Meta:
#         model = HospitalProfile
#         fields = ['user__username', 'user__email', 'user__first_name', 'user__last_name', 'address', 'profile_picture']

# class EditPatientProfileForm(UserChangeForm):
#     class Meta:
#         model = PatientsProfile
#         fields = ['user__username', 'user__email', 'user__first_name', 'user__last_name', 'address', 'profile_picture']

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name')

class EditHospitalProfileForm(forms.ModelForm):
    username = forms.CharField(label='Username', disabled=False,required=True, widget=forms.TextInput(attrs={'placeholder': 'Username', 'class': 'form-control'}))
    email = forms.EmailField(required=True,disabled=True, label='Email', widget=forms.TextInput(attrs={'placeholder': 'Email', 'class': 'form-control'}))
    first_name = forms.CharField(label='First Name', required=False, widget=forms.TextInput(attrs={'placeholder': 'first name', 'class': 'form-control'}))
    last_name = forms.CharField(label='Last Name', required=False, widget=forms.TextInput(attrs={'placeholder': 'last name', 'class': 'form-control'}))
    phone = forms.CharField(label='Phone Number', required=False, widget=forms.TextInput(attrs={'placeholder': 'Phone Number', 'class': 'form-control'}))
    
    class Meta:
        model = HospitalProfile
        fields = ['address', 'profile_picture', 'username','first_name', 'last_name', 'email','phone']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Populate initial values for the user fields from the related user instance
        if self.instance.user:
            self.fields['username'].initial = self.instance.user.username
            self.fields['email'].initial = self.instance.user.email
            self.fields['first_name'].initial = self.instance.user.first_name
            self.fields['last_name'].initial = self.instance.user.last_name
            self.fields['phone'].initial = self.instance.user.phone
        
        # Populate initial value for the address field from the related hospital profile instance
        if self.instance.address:
            self.fields['address'].initial = self.instance.address
    def clean_username(self):
        username = self.cleaned_data['username']
        if User.objects.exclude(pk=self.instance.user.pk).filter(username=username).exists():

            raise forms.ValidationError("Username already exists. Please choose a different one.")
        return username

    def save(self, commit=True):
        # Update the user's username
        self.instance.user.username = self.cleaned_data['username']
        self.instance.user.first_name = self.cleaned_data['first_name']
        self.instance.user.last_name = self.cleaned_data['last_name']
        self.instance.user.phone = self.cleaned_data['phone']
        self.instance.user.save()
        return super().save(commit)

class EditPatientProfileForm(forms.ModelForm):
    username = forms.CharField(label='Username', disabled=False,required=True, widget=forms.TextInput(attrs={'placeholder': 'Username', 'class': 'form-control'}))
    email = forms.EmailField(required=True,disabled=True, label='Email', widget=forms.TextInput(attrs={'placeholder': 'Email', 'class': 'form-control'}))
    first_name = forms.CharField(label='First Name', required=False, widget=forms.TextInput(attrs={'placeholder': 'first name', 'class': 'form-control'}))
    last_name = forms.CharField(label='Last Name', required=False, widget=forms.TextInput(attrs={'placeholder': 'last name', 'class': 'form-control'}))
    phone = forms.CharField(label='Phone Number', required=False, widget=forms.TextInput(attrs={'placeholder': 'Phone Number', 'class': 'form-control'}))
    
    class Meta:
        model = PatientsProfile
        fields = ['address', 'profile_picture', 'username','first_name', 'last_name', 'email','phone']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Populate initial values for the user fields from the related user instance
        if self.instance.user:
            self.fields['username'].initial = self.instance.user.username
            self.fields['email'].initial = self.instance.user.email
            self.fields['first_name'].initial = self.instance.user.first_name
            self.fields['last_name'].initial = self.instance.user.last_name
            self.fields['phone'].initial = self.instance.user.phone
        
        # Populate initial value for the address field from the related hospital profile instance
        if self.instance.address:
            self.fields['address'].initial = self.instance.address
    def clean_username(self):
        username = self.cleaned_data['username']
        if User.objects.exclude(pk=self.instance.user.pk).filter(username=username).exists():
            raise forms.ValidationError("Username already exists. Please choose a different one.")
        return username

    def save(self, commit=True):
        # Update the user's username
        self.instance.user.username = self.cleaned_data['username']
        self.instance.user.first_name = self.cleaned_data['first_name']
        self.instance.user.last_name = self.cleaned_data['last_name']
        self.instance.user.phone = self.cleaned_data['phone']
        self.instance.user.save()
        return super().save(commit)



