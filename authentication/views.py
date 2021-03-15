# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.forms.utils import ErrorList
from django.http import HttpResponse
from .forms import LoginForm, SignUpForm
import sqlite3
import datetime

def home_view(request):
    form = LoginForm(request.POST or None)

    msg = None

    if request.method == "POST":

        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect("/")
            else:
                msg = 'Invalid credentials'
        else:
            msg = 'Error validating the form'

    return render(request, "accounts/homepage.html", {"form": form, "msg" : msg})


def login_view(request):
    form = LoginForm(request.POST or None)

    msg = None



    if request.method == "POST":

        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect("/")
            else:    
                msg = 'Invalid credentials'    
        else:
            msg = 'Error validating the form'    

    return render(request, "accounts/login.html", {"form": form, "msg" : msg})

def register_user(request):

    msg     = None
    success = False
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get("username")
            raw_password = form.cleaned_data.get("password1")
            user = authenticate(username=username, password=raw_password)

            msg     = 'User created - please <a href="/login">login</a>.'
            success = True
            
            #return redirect("/login/")

        else:
            msg = 'Form is not valid'    
    else:
        form = SignUpForm()

    return render(request, "accounts/register.html", {"form": form, "msg" : msg, "success" : success })

def insert_request_to_sqlite(request_website, request_username, request_password, request_price, request_description, request_accept_checkbox, request):
    
    # print('user_id : ' + str(request.user.id ))

    onn = None

    db_file = 'db.sqlite3'
    try:

        conn = sqlite3.connect(db_file)
        c = conn.cursor()

        ################################ Insert to Requests Table #################################
        c.execute(" INSERT INTO auth_requests(user_id, website, username, password, price, description, status, time_slot) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
         (str(request.user.id),
         str(request_website),
         str(request_username),
         str(request_password),
         str(request_price),
         str(request_description),
         "PENDING",
         datetime.datetime.now()
         )
         )

        conn.commit()

        c.close()
        conn.close()
        print('Request inserted successfully !!!')

    except Exception as e:
        print('Unsuccessful insertion !!!')
        print(e)
        return 'Fail'


    return 'Success'

def insert_request(request):
    msg = None
    success = False


    if request.method == "POST":

        form = LoginForm(request.POST or None)
        

        request_website = request.POST.get('website_input')
        request_username = request.POST.get('username_input')
        request_password = request.POST.get('password_input')
        request_price = request.POST.get('price_input')
        request_description = request.POST.get('description_input')
        request_accept_checkbox = request.POST.get('accept_checkbox_input')

        msg = insert_request_to_sqlite(request_website, request_username, request_password, request_price, request_description, request_accept_checkbox, request)

        # print("website   :" + str(request_website))
        # print("username   :" + str(request.POST.get('username_input')))
        # print("pass   :" + str(request.POST.get('password_input')))
        # print("price   :" + str(request.POST.get('price_input')))
        # print("description   :" + str(request.POST.get('description_input')))
        # print("checkbox   :" + str(request.POST.get('accept_checkbox_input')))



        msg = 'Request inserted - please <a href="/login">login</a>.'

    else:
        pass
    return render(request, "requests.html", {"form": form, "msg": msg, "success": success})
