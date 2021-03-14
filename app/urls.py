# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django.urls import path, re_path
from app import views

urlpatterns = [

    # The home page
    path('', views.home, name='home'),
    # The requests page
    path('', views.requests, name='requests'),

    # Matches any html file
    re_path(r'^.*\.*', views.pages, name='pages'),

]
