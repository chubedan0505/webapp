from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('',views.loginPage,name="login"),
    path('homechat/',views.homechat,name="homechat"),
    path('edit/',views.edit,name="edit"),
    path('checkout', views.checkout,name="checkout"),
    path('login/',views.loginPage,name="login"),
    path('logout/',views.logoutPage,name="logout"),
    path('register/',views.register,name="register"),
    path('profile/',views.profile,name="profile"),
    #path('confirm/<str:uidb64>/<str:token>/', views.confirm_email, name='confirm_email'),
    #path('Email/',views.Email,name="Email"),
]
