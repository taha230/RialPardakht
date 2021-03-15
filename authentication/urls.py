# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django.urls import path
from .views import login_view, register_user, home_view, insert_request, dashboard_view, requests_view
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('home/', home_view, name="home"),
    path('dashboard/', dashboard_view, name="dashboard"),
    path('requests/', requests_view , name="requests"),
    path('login/', login_view, name="login"),
    path('register/', register_user, name="register"),
    path("logout/", home_view, name="logout"),
    path("requests/", insert_request, name="requests")

]
