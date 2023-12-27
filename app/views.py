from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm
from .models import *
from django.contrib import messages
from django.core.mail import send_mail
from django.utils.html import strip_tags
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.urls import reverse
from django.template.loader import render_to_string
from django.contrib.auth import authenticate, login, logout


def home(request):
    context = {}
    return render(request, 'app/home.html', context)


def Email(request):
    if request.user.is_authenticated:
        context = {}
        return render(request, 'app/Email.html', context)


# Create your views here.
def homechat(request):
    #  if request.user.is_authenticated:
    context = {}
    return render(request, 'app/homechat.html', context)


#   else :
#          return redirect('login')

# Create your views here.
def cart(request):
    context = {}
    return render(request, 'app/cart.html', context)


def checkout(request):
    context = {}
    return render(request, 'app/checkout.html', context)


def register(request):
    form = CreateUserForm()
    if request.method == "POST":
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
        return redirect('login')
    context = {'form': form}
    return render(request, 'app/register.html', context)


#  if request.method == 'POST':
#     form = CreateUserForm(request.POST)
#    if form.is_valid():
#       user = form.save(commit=False)
#      user.is_active = False  # Đánh dấu tài khoản chưa được kích hoạt
#     user.save()
#    send_confirmation_email(request, user)  # Gửi email xác nhận
#    return render(request, 'app/login.html')
# else:
# form = CreateUserForm()
# return render(request, 'app/register.html', {'form': form})


def logoutPage(request):
    logout(request)
    return redirect('login')


def edit(request):
    context = {}
    return render(request, 'app/edit.html', context)


def profile(request):
    context = {}
    return render(request, 'app/profile.html', context)


def loginPage(request):
    if request.user.is_authenticated:
        return redirect('homechat')
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('homechat')

        else:
            messages.info(request, 'user or password not correct!')
    context = {}
    return render(request, 'app/login.html', context)


def show_user_profile(request, user_id):
    user = CustomUser.objects.get(pk=user_id)
    return render(request, 'user_profile.html', {'user': user})
