from django.contrib import admin
from .models import *

# Register your models here.

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'user_type',)

admin.site.register(HospitalProfile)
admin.site.register(PatientsProfile)