from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.models import User
from .models import Profile
from .forms import UserRegistration, UserUpdateForm, ProfileUpdateForm
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from email.message import EmailMessage
import smtplib
from django.conf import settings

def register(request):
    msg = EmailMessage()
    if request.method == "POST":
        form = UserRegistration(request.POST)
        if form.is_valid():
            user_email = form.cleaned_data.get('email')
            username = form.cleaned_data.get('user')
            if User.objects.filter(email=user_email).exists():
                messages.info(request, f"Sorry,a user with the same email already exists.")
            else:
                form.save()
                msg['SUbject'] = "Welcome to Let's sing acapella."
                msg['From'] = settings.EMAIL_HOST_USER
                msg['TO'] = user_email
                msg.set_content(f"{username},hi,music is like the food to the soul when it comes to us.We don't know about you but since you have registered here it means we are on the same page.What we want to say to you is that here we make acapella look real and entertaining.Just stay blessed and sing.")
                hml = f"""
                <!Doctype html>
                <html>
                <body>
                <h1 style='font-style:italic;'>Let's Sing Acapella.</h1>
                <p style='color:SlateGray;'> {username},hi,music is like the food to the soul when it comes to us.We don't know about you but since you have registered here it means we are on the same page.What we want to say to you is that here we make acapella look real and entertaining.Just stay blessed and sing. </p>
                <p style='color:SlateGray;'>The Let's Sing Acapella Team.</p>
                </body>
                </html>
                </html>
                """
                msg.add_alternative(hml, subtype='html')
                with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
                    smtp.login(settings.EMAIL_HOST_USER,settings.EMAIL_HOST_PASSWORD)
                    smtp.send_message(msg)
                    messages.success(request, f"{username}, your account is created.")
                    return redirect('login')
    else:
        form = UserRegistration()

    context = {
        'form': form
    }
    return render(request, "users/register.html", context)


def login_request(request):
    if request.method == "POST":
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('main')
            else:
                messages.info(request, f"username or password invalid")
        else:
            messages.info(request, f"Invalid details")
    else:
        form = AuthenticationForm()
    context = {
        'form': form
    }

    return render(request, "users/login.html", context)


def logout(request):
    return render(request, "users/logout.html")


@login_required()
def profile(request):
    if request.method == "POST":
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            return redirect('profile')
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)

    context = {
        'u_form': u_form,
        'p_form': p_form
    }
    return render(request, "users/profile.html", context)
