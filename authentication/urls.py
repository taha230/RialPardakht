# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django.urls import path
from .views import login_view, register_user, home_view, insert_request_to_db, dashboard_view, requests_view, ticket_view, insert_ticket_to_db
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('home/', home_view, name="home"),
    path('dashboard/', dashboard_view, name="dashboard"),
    path('requests/', requests_view , name="requests"),
    path('tickets/', ticket_view , name="tickets"),
    path('login/', login_view, name="login"),
    path('register/', register_user, name="register"),
    path("logout/", home_view, name="logout"),
    path("tickets_call_back_insert/", insert_ticket_to_db, name="tickets"),
    path("requests_call_back_insert/", insert_request_to_db, name="requests")

]
