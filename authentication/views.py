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
                return redirect("/home")
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
                return redirect("/dashboard/")
            else:    
                msg = 'Invalid credentials'    
        else:
            msg = 'Error validating the form'    

    return render(request, "accounts/login.html", {"form": form, "msg" : msg, 'c1': 'ali'})

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

            msg     = 'User created - please <a href="/login/">login</a>.'
            success = True
            
            #return redirect("/login/")

        else:
            msg = 'Form is not valid'    
    else:
        form = SignUpForm()

    return render(request, "accounts/register.html", {"form": form, "msg" : msg, "success" : success })

def get_request_list_from_sqlite_by_user_id(request):
    
    onn = None

    db_file = 'db.sqlite3'
    try:

        conn = sqlite3.connect(db_file)
        c = conn.cursor()

        ################################ Select from Requests Table #################################
        c.execute(" SELECT * FROM auth_requests WHERE user_id=?", (str(request.user.id)))

        row_list = []

        pending_count = 0
        processed_count = 0
        total_count = 0

        digikala_count = 0
        namava_count = 0
        filimo_count = 0
        other_website_count = 0

        for row in list(c):
            if (len(row) == 9):

                row_json = {}
                row_json['id'] = row[0]
                row_json['user_id'] = row[1]
                row_json['website'] = row[2]
                row_json['username'] = row[3]
                row_json['password'] = row[4]
                row_json['price'] = row[5]
                row_json['description'] = row[6]
                row_json['status'] = row[7]
                row_json['time_slot'] = row[8]

                row_list.append(row_json)

                ########### check count ############################
                if (row_json['status'] == 'PENDING'):
                    pending_count += 1
                else:
                    processed_count += 1
                total_count += 1

                ############ check website ##########################
                if ('digikala' in row_json['website']):
                    digikala_count += 1
                elif ('namava' in row_json['website']):
                    namava_count += 1
                elif ('filimo' in row_json['website']):
                    filimo_count += 1
                else :
                    other_website_count += 1



        c.close()
        conn.close()
        print('Request select successfully from user_id ' + str(request.user.id) + ' !!!')

        return row_list, total_count, pending_count, processed_count, digikala_count, namava_count, filimo_count, other_website_count

    except Exception as e:
        print('Unsuccessful selection !!!')
        print(e)
        return [], 0, 0, 0, 0, 0, 0, 0

def get_ticket_list_from_sqlite_by_user_id(request):
    
    onn = None

    db_file = 'db.sqlite3'
    try:

        conn = sqlite3.connect(db_file)
        c = conn.cursor()

        ################################ Select from Tickets Table #################################
        c.execute(" SELECT * FROM auth_tickets WHERE user_id=?", (str(request.user.id)))

        row_list = []

        pending_count = 0
        answered_count = 0
        total_count = 0


        for row in list(c):
            if (len(row) == 6):

                row_json = {}
                row_json['id'] = row[0]
                row_json['user_id'] = row[1]
                row_json['body'] = row[2]
                row_json['answer'] = row[3]
                row_json['status'] = row[4]
                row_json['time_slot'] = row[5]

                row_list.append(row_json)

                ########### check count ############################
                if (row_json['status'] == 'PENDING'):
                    pending_count += 1
                else:
                    answered_count += 1
                total_count += 1

                



        c.close()
        conn.close()
        print('Request select successfully from user_id ' + str(request.user.id) + ' !!!')

        return row_list, total_count, pending_count, answered_count

    except Exception as e:
        print('Unsuccessful selection !!!')
        print(e)
        return [], 0, 0, 0, 0, 0, 0, 0

def get_request_list_from_sqlite_all():
    
    onn = None

    db_file = 'db.sqlite3'
    try:

        conn = sqlite3.connect(db_file)
        c = conn.cursor()

        ################################ Select from Requests Table #################################
        c.execute(" SELECT * FROM auth_requests")

        row_list_all = []
        row_list_pending = []
        row_list_processed = []


        pending_count = 0
        processed_count = 0
        total_count = 0

        digikala_count = 0
        namava_count = 0
        filimo_count = 0
        other_website_count = 0

        for row in list(c):
            if (len(row) == 9):

                row_json = {}
                row_json['id'] = row[0]
                row_json['user_id'] = row[1]
                row_json['website'] = row[2]
                row_json['username'] = row[3]
                row_json['password'] = row[4]
                row_json['price'] = row[5]
                row_json['description'] = row[6]
                row_json['status'] = row[7]
                row_json['time_slot'] = row[8]

                row_list_all.append(row_json)

                ########### check count ############################
                if (row_json['status'] == 'PENDING'):
                    pending_count += 1
                    row_list_pending.append(row_json)
                else:
                    processed_count += 1
                    row_list_processed.append(row_json)

                total_count += 1

                ############ check website ##########################
                if ('digikala' in row_json['website']):
                    digikala_count += 1
                elif ('namava' in row_json['website']):
                    namava_count += 1
                elif ('filimo' in row_json['website']):
                    filimo_count += 1
                else :
                    other_website_count += 1



        c.close()
        conn.close()
        print('All request select successfully !!!')

        return row_list_all, row_list_pending, row_list_processed, total_count, pending_count, processed_count, digikala_count, namava_count, filimo_count, other_website_count

    except Exception as e:
        print('Unsuccessful selection !!!')
        print(e)
        return [], [], [], 0, 0, 0, 0, 0, 0, 0

def get_ticket_list_from_sqlite_all():
    
    onn = None

    db_file = 'db.sqlite3'
    try:

        conn = sqlite3.connect(db_file)
        c = conn.cursor()

        ################################ Select from Tickets Table #################################
        c.execute(" SELECT * FROM auth_tickets")

        row_list_all = []
        row_list_pending = []
        row_list_answered = []


        pending_count = 0
        answered_count = 0
        total_count = 0

        for row in list(c):
            if (len(row) == 6):

                row_json = {}
                row_json['id'] = row[0]
                row_json['user_id'] = row[1]
                row_json['body'] = row[2]
                row_json['answer'] = row[3]
                row_json['status'] = row[4]
                row_json['time_slot'] = row[5]

                row_list_all.append(row_json)

                ########### check count ############################
                if (row_json['status'] == 'PENDING'):
                    pending_count += 1
                    row_list_pending.append(row_json)
                else:
                    answered_count += 1
                    row_list_answered.append(row_json)

                total_count += 1

               


        c.close()
        conn.close()
        print('All request select successfully !!!')

        return row_list_all, row_list_pending, row_list_answered, total_count, pending_count, answered_count

    except Exception as e:
        print('Unsuccessful selection !!!')
        print(e)
        return [], [], [], 0, 0, 0, 0, 0, 0, 0

def insert_request_to_sqlite(request_website, request_username, request_password, request_price, request_description, request_accept_checkbox, request):
    
    # print('user_id : ' + str(request.user.id ))

    conn = None

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

def insert_ticket_to_sqlite(request_body, request):
    
    conn = None

    db_file = 'db.sqlite3'
    try:

        conn = sqlite3.connect(db_file)
        c = conn.cursor()

        ################################ Insert to Tickets Table #################################
        c.execute(" INSERT INTO auth_tickets(user_id, body, answer, status, time_slot) VALUES (?, ?, ?, ?, ?)",
         (str(request.user.id),
         str(request_body),
         "",
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

def insert_request_to_db(request):
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
        # request_list, total_count, pending_count, processed_count, digikala_count, namava_count, filimo_count, other_website_count = get_request_list_from_sqlite_by_user_id(request)
        # request_list_all, request_list_pending, request_list_processed, total_count, pending_count, processed_count, digikala_count, namava_count, filimo_count, other_website_count = get_request_list_from_sqlite_all()

    else:
        pass
    return render(request, "request_insert_result.html", {"form": form, "msg": msg, "success": success})

def insert_ticket_to_db(request):
    msg = None
    success = False


    if request.method == "POST":

        form = LoginForm(request.POST or None)
        

        ticket_body = request.POST.get('body_input')
    

        msg = insert_ticket_to_sqlite(ticket_body, request)

    else:
        pass
    return render(request, "ticket_insert_result.html", {"form": form, "msg": msg, "success": success})

def dashboard_view(request):

    form = LoginForm(request.POST or None)
    msg = None
    row_list_request, total_count_request, pending_count_request, processed_count_request, digikala_count, namava_count, filimo_count, other_website_count = get_request_list_from_sqlite_by_user_id(request)
    row_list_ticket, total_count_ticket, pending_count_ticket, answered_count_ticket = get_ticket_list_from_sqlite_by_user_id(request)
    
    if (total_count_request != 0):
        digikala_percent = int(digikala_count / total_count_request* 100)
        namava_percent = int(namava_count / total_count_request * 100)
        filimo_percent = int(filimo_count / total_count_request * 100)
        other_website_percent = int(other_website_count / total_count_request * 100)
    else:
        digikala_percent = 0
        namava_percent = 0
        filimo_percent = 0
        other_website_percent = 0

    context = {'row_list': row_list_request,
              'total_count': total_count_request,
              'pending_count': pending_count_request,
              'processed_count': processed_count_request,
              'total_count_ticket': total_count_ticket,
              'pending_count_ticket': pending_count_ticket,
              'answered_count_ticket': answered_count_ticket,
              'digikala_count': digikala_count,
              'namava_count': namava_count,
              'filimo_count': filimo_count,
              'other_website_count': other_website_count,
              'digikala_percent': digikala_percent,
              'namava_percent': namava_percent,
              'filimo_percent': filimo_percent,
              'other_website_percent': other_website_percent,
              "form": form, "msg" : msg
              }
    return render(request, "index.html", context)

def requests_view(request):

    form = LoginForm(request.POST or None)
    msg = None
    row_list, total_count, pending_count, processed_count, digikala_count, namava_count, filimo_count, other_website_count = get_request_list_from_sqlite_by_user_id(request)
    if (total_count != 0):
        digikala_percent = int(digikala_count / total_count* 100)
        namava_percent = int(namava_count / total_count * 100)
        filimo_percent = int(filimo_count / total_count * 100)
        other_website_percent = int(other_website_count / total_count * 100)
    else:
        digikala_percent = 0
        namava_percent = 0
        filimo_percent = 0
        other_website_percent = 0

    context = {'row_list': row_list,
              'total_count': total_count,
              'pending_count': pending_count,
              'processed_count': processed_count,
              'digikala_count': digikala_count,
              'namava_count': namava_count,
              'filimo_count': filimo_count,
              'other_website_count': other_website_count,
              'digikala_percent': digikala_percent,
              'namava_percent': namava_percent,
              'filimo_percent': filimo_percent,
              'other_website_percent': other_website_percent,
              "form": form, "msg" : msg
              }
    return render(request, "requests.html", context)

def ticket_view(request):

    form = LoginForm(request.POST or None)
    msg = None
    row_list, total_count, pending_count, answered_count = get_ticket_list_from_sqlite_by_user_id(request)
    

    context = {'row_list': row_list,
              'total_count_ticket': total_count,
              'pending_count_ticket': pending_count,
              'answered_count_ticket': answered_count,
              
              "form": form, "msg" : msg
              }
    return render(request, "tickets.html", context)
