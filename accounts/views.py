from django.shortcuts import render, redirect, HttpResponseRedirect, HttpResponse
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from .models import User
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from .form import RegisterForm, LoginForm, CustomUserChangeForm, CustomPasswordChangeForm, CustomPasswordResetForm
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.decorators import login_required
# Create your views here.

# Send email Token
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from .tokens import account_activation_token
from django.core.mail import EmailMessage

from .models import User as UserModel


def login(request):
    # if (request.user.is_authenticated):
    #     return redirect("index")
    if request.method == "GET":
        next = ''
        if 'next' in request.GET:
            next = request.GET['next']
        form = LoginForm()
        return render(request, 'accounts/login.html', {'form': form, 'next': next})
    form = LoginForm(request.POST)
    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(request, username=username, password=password)
    if user is not None:
        auth_login(request, user)
        next_url = request.GET.get('next')

        if next_url:
            return HttpResponseRedirect(next_url)
        else:
            return redirect('/')
    return render(request, 'accounts/login.html', {'form': form, 'title': 'Login'})


def logout(request):
    auth_logout(request)
    return redirect('/accounts/login')


def register(request):
    if (request.user.is_authenticated):
        return redirect("index")

    if request.method == "GET":
        form = RegisterForm()
        return render(request, 'accounts/register.html', {'form': form})

    form = RegisterForm(request.POST)
    if form.is_valid():
        user = form.save(commit=False)
        user.is_active = False
        user.save()
        current_site = get_current_site(request)
        mail_subject = 'Activate your blog account.'
        message = render_to_string('accounts/acc_active_email.html', {
            'user': user,
            'domain': current_site.domain,
            'uid': urlsafe_base64_encode(force_bytes(user.pk)),
            'token': account_activation_token.make_token(user),
        })
        to_email = form.cleaned_data.get('email')
        email = EmailMessage(
            mail_subject, message, to=[to_email]
        )
        email.send()
        return HttpResponse('Please confirm your email address to complete the registration')
        return redirect('/')
    return render(request, 'accounts/register.html', {'form': form})


@login_required
def profile(request):
    if request.method == "GET":
        form = CustomUserChangeForm(instance=request.user)
        return render(request, 'accounts/profile.html', {'form': form})

    form = CustomUserChangeForm(data=request.POST, instance=request.user)
    if form.is_valid():
        user = form.save(commit=False)
        user.save()
    return redirect('/accounts/profile')


# @login_required
# def change_password(request):
#     if request.method == 'GET':
#         form = CustomPasswordChangeForm(request.user)
#         return render(request, 'accounts/change-password.html', {'form': form})

#     form = CustomPasswordChangeForm(request.user, request.POST)
#     if form.is_valid():
#         print("--------------------------------------")
#         print("Form is valid")
#         user = form.save(commit=False)
#         update_session_auth_hash(request, user)
#         user.save()
#         return redirect('/accounts/update-profile')
#     messages.error(request, 'Please correct the error below.')
#     return render(request, 'accounts/change-password.html', {'form': form})


# def reset_password(request):
#     if request.method == 'GET':
#         form = CustomPasswordResetForm()
#         return render(request, 'accounts/reset-password.html', {'form': form})


def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = UserModel.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, UserModel.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        auth_login(request, user)
        # return redirect('home')
        return HttpResponse('Thank you for your email confirmation. Now you can login your account.')
    else:
        return HttpResponse('Activation link is invalid!')
