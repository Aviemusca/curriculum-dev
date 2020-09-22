from django.urls import reverse_lazy
from django.shortcuts import render, redirect

from django.contrib.auth.decorators import login_required
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages

from django.views.generic import CreateView
from django.contrib.auth.views import LoginView

from .models import CustomUser
from curricula.models import Curriculum

from .forms import (
        CustomUserCreationForm,
        CustomUserChangeForm,
        ProfileChangeForm
        )


class SignUpView(SuccessMessageMixin, CreateView):
    model = CustomUser
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('login')
    success_message = "Account created for %(username)s! You are now able to sign in."
    template_name = 'signup.html'

    def get_success_message(self, cleaned_data):
        return self.success_message % dict(
                cleaned_data,
                username=self.object.username,
                )


class CustomLoginView(LoginView):

    def get_success_url(self):
        """ Redirect the user to the home page if they have no curriculum
        yet, else to their curriculum list"""
        if Curriculum.objects.filter(author=self.request.user).count() > 0:
            return reverse_lazy('curricula:user', kwargs={'username': self.request.user.username})
        else:
            return reverse_lazy('pages:home')


@login_required
def profile(request):
    if request.method == "POST":
        u_form = CustomUserChangeForm(request.POST, instance=request.user)
        p_form = ProfileChangeForm(request.POST, request.FILES, instance=request.user.profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, f"Your account has been updated!")
            return redirect('profile')
    else:
        u_form = CustomUserChangeForm(instance=request.user)
        p_form = ProfileChangeForm(instance=request.user.profile)
    context = {
            'u_form': u_form,
            'p_form': p_form,
            }
    return render(request, 'profile.html', context)
