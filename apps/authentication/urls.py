# -*- encoding: utf-8 -*-
"""
Copyright (c) 2024 - Capgemini Team AI Bytes
"""

from django.contrib.auth.views import LogoutView
from django.urls import path

from .views import login_view, register_user

urlpatterns = [
    path('login/', login_view, name="login"),
    path('register/', register_user, name="register"),
    path("logout/", LogoutView.as_view(), name="logout")
]
