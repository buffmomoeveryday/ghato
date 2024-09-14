from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import make_password
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from icecream import ic

from tenant.models import TenantModel
from users.models import CustomUser

from fbv.decorators import render_html


def login_user(request):
    if request.method == "GET":
        return render(request, "users/login.html")

    if request.method == "POST":
        tenant = request.tenant

        email = request.POST.get("email")
        password = request.POST.get("password")
        ic(password)

        user = authenticate(username=email, password=password)
        ic(user)

        if user is not None:
            if user.is_active:
                ic(user.tenant)
                ic(request.tenant)
                if user.tenant == tenant:
                    login(request, user)
                    messages.success(request, "Success")
                    return redirect(reverse_lazy("dashboard_index"))
                else:
                    messages.error(request, "Invalid tenant.")
            else:
                messages.error(request, "User account is inactive.")
        else:
            messages.error(request, "Invalid credentials.")

        return redirect(reverse_lazy("login"))


def register_user(request):
    if request.method == "GET":
        return render(request=request, template_name="users/register.html")

    if request.method == "POST":
        email = request.POST.get("email")
        password1 = request.POST.get("password1")
        password2 = request.POST.get("password2")
        company_name = request.POST.get("company_name")
        domain = request.POST.get("domain")

        if password1 != password2:
            messages.error(request=request, message="Password Error")
            return redirect(reverse_lazy("register"))

        if CustomUser.objects.filter(email=email).exists():
            messages.error(request=request, message="Email Already Exists")
            return redirect(reverse_lazy("register"))

        if TenantModel.objects.filter(domain=domain.lower()).exists():
            messages.error(request=request, message="Domain Name Already Exists")
            return redirect(reverse_lazy("register"))

        tenant = TenantModel.objects.create(
            name=company_name,
            domain=domain,
        )
        tenant.save()
        user = CustomUser.objects.create(
            email=email,
            password=make_password(password=password1),
        )
        user.save()
        messages.success(request=request, message="Registered Successfully")
        return redirect(reverse_lazy("login"))


def logout_user(request):
    logout(request)
    return redirect("login")


@login_required
def settings(request):
    if request.method == "GET":
        employees = CustomUser.objects.filter(tenant=request.tenant).exclude(
            id=request.user.id
        )

        context = {
            "employees": employees,
        }
        return render(
            request=request,
            template_name="users/settings.html",
            context=context,
        )

    if request.method == "POST":
        email = request.POST.get("email")
        password1 = request.POST.get("password1")
        password2 = request.POST.get("password2")
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")

        if password1 or password2:
            if password1 != password2:
                messages.error(request=request, message="Passwords do not match.")
                return redirect(reverse_lazy("user_settings"))

        if CustomUser.objects.filter(email=email).exclude(pk=request.user.pk).exists():
            messages.error(request=request, message="Email already exists.")
            return redirect(reverse_lazy("user_settings"))

        user = request.user
        user.email = email
        user.first_name = first_name
        user.last_name = last_name

        if password1 and password2:
            user.password = make_password(password=password1)

        user.save()
        messages.success(request, "Settings updated successfully.")
        return redirect(reverse_lazy("user_settings"))


@login_required
def add_new_users(request):
    if request.htmx and request.method == "GET":
        return render(request=request, template_name="")
