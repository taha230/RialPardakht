# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django.urls import path
from .views import login_view, register_user, home_view, insert_request
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('home/', home_view, name="home"),
    path('login/', login_view, name="login"),
    path('register/', register_user, name="register"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("requests/", LogoutView.as_view(), name="requests")
]
