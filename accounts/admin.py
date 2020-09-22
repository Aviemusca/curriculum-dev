from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import CustomUser, Profile
from .forms import CustomUserCreationForm, CustomUserChangeForm

class CustomUserAdmin(UserAdmin):
    model = CustomUser
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    display_list = ['username', 'email']

admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Profile)
