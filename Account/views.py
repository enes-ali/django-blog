from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.views.generic import View
from .forms import *
from django.http import HttpResponse
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required

class LoginPage(View):

    def get(self, request):
        return render(request, "Account/login.html")

    def post(self, request):
        email = request.POST.get("email")
        password = request.POST.get("password")

        user = authenticate(email=email, password=password)
        if user is not None:
            login(request, user)
            return redirect("/admin/")

        else:
            return render(request, "Account/login.html", {"errors": ["Invalid Email or Password"]})


class RegisterPage(View):

    def get(self, request):
        form = UserRegisterForm()
        return render(request, "Account/register.html", {"form": form})

    def post(self, request):
        user_form = UserRegisterForm(request.POST)
        if user_form.is_valid():
            new_user = user_form.save()
            
            user = authenticate(email=user_form.cleaned_data['email'], password=user_form.cleaned_data["password"])
            if user is not None:
                login(request, user)
                return redirect("/admin/")

        else:
            return render(request, "Account/register.html", {"form": user_form})


@require_POST
@login_required(login_url="/", redirect_field_name="")
def Logout(request):
    redirect_url = request.POST.get("redirect_to")
    logout(request)
    return redirect(redirect_url)
