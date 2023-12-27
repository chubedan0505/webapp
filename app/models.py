from django.db import models
from django.contrib.auth.models import User
# Create your models here.
from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth.models import AbstractUser


class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'password1', 'password2']
