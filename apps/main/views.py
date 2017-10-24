# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from models import *
from django.shortcuts import render, redirect
from django.contrib import messages
import bcrypt

def index(request):
    return render(request, 'main/index.html')

def process(request):
    errors = User.objects.validator(request.POST)
    if errors:
        for error in errors:
            messages.error(request, errors[error])
        return redirect('/')
    else:
        hashed_pw = hashed_pw = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt())
        user = User.objects.create(name=request.POST['name'], alias=request.POST['alias'],email=request.POST['email'], password=hashed_pw, bday=request.POST['birthday'])
        request.session['id'] = user.id
        request.session['name']= user.name
        return redirect('/dashboard')

def login(request):
    login_return = User.objects.login(request.POST)
    if 'user' in login_return:
        request.session['id'] = login_return['user'].id
        request.session['name']= login_return['user'].name
        return redirect('/dashboard')
    else:
        messages.error(request, login_return['errors'])
        return redirect('/')


def dashboard(request):
    try:
        request.session['id']
    except KeyError:
        return redirect('/')

    context = {
        #Quotes.objects.exclude(related_name).all() == so you do not see your own
        # Quotes.objects.fiilter(related_name) ==> favorite quote 
        'quotes': Quote.objects.all(),
        'favorite': User.objects.get(id=request.session['id']).quotes.all()
    }
    return render(request, 'main/quotes.html', context)


def users(request, user_id): 
    context = {
        "User": User.objects.filter(id=user_id),
        'Quotes': Quote.objects.all()

        # "quotes": Quote.
    }
    return render(request, 'main/users.html', context)

def favorite (request, quote_id): 
    a = Quote.objects.get(id=quote_id)
    User.objects.get(id=request.session['id']).quotes.add(a)
    return redirect('/dashboard')

def remove(request, quote_id):
    a = Quote.objects.get(id=quote_id)
    User.objects.get(id=request.session['id']).quotes.delete(a)
    return redirect('/dashboard')

def newquote (request):
    q_errors = Quote.objects.quote_validator(request.POST)
    if q_errors:
        for error in q_errors:
            messages.error(request, q_errors[error])
        return redirect('/dashboard')
    else:
        quote = Quote.objects.create(quoted_by=request.POST['quoted'], message=request.POST['msg'],user_id=request.session['id'])
        return redirect('/dashboard')
        
def logout(request):
    del request.session['id']
    del request.session['name']
    return redirect('/')
