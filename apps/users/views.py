# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render, redirect
from django.core.urlresolvers import reverse
from .models import User, Poke
from django.db.models import Count, Sum
import bcrypt
from django.contrib import messages

def pokes(request):
    if 'loggedin' not in request.session:
        return redirect(reverse('logreg'))
    else:
        ut = User.objects.get(id=request.session['loggedin'])
        pt = Poke.objects.filter(poked_id=ut).order_by("times")
        wpmt = []
        for element in pt:
            pmut = User.objects.get(id=element.poker_id.id)
            wpmt.append({'alias':pmut.alias, 'times':element.times})
        otherut = User.objects.exclude(id=request.session['loggedin'])
        otherutb = []
        for user in otherut:
            phc = 0
            phuct = Poke.objects.filter(poked_id=user)
            for poke in phuct:
                phc += poke.times
            otherutb.append({'user':user,'times_poked':phc}) 
        context = {
            'user': ut,
            'whopokedme': wpmt,
            'pokedmecount' : len(wpmt),
            'otherusers': otherutb,
        }
        return render(request, 'users/pokes.html', context)

def logreg(request):
    if 'loggedin' in request.session:
        return redirect(reverse('pokes'))
    else:
        return render(request, 'users/logreg.html')

def register(request):
    if request.method == "POST":
        errors = User.objects.validator(request.POST)
        if len(errors):
            for tag, error in errors.iteritems():
                messages.error(request, error, extra_tags="register")
        else:
            pwt = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt())
            User.objects.create(name=request.POST['name'], alias=request.POST['alias'], email=request.POST['email'], pw_hash=pwt, dob=request.POST['dateob'])
            ut = User.objects.filter(pw_hash=pwt)[0]
            request.session['loggedin'] = ut.id
            ut = None
            pwt = None
    return redirect(reverse('pokes'))

def login(request):
    if request.method == "POST":
        errors = User.objects.logvalid(request.POST)
        if len(errors):
            for tag, error in errors.iteritems():
                messages.error(request, error, extra_tags="login")
        else:
            ut = User.objects.filter(email=request.POST['email'])[0]
            request.session['loggedin'] = ut.id
            ut = None
    return redirect(reverse('pokes'))

def logout(request):
    request.session.pop('loggedin')
    return redirect(reverse('pokes'))

def addpoke(request):
    if request.method == "POST":
        pokert = User.objects.get(id=request.POST['poker'])
        pokedt = User.objects.get(id=request.POST['poked'])
        pt = Poke.objects.filter(poked_id=pokedt.id, poker_id=pokert.id)
        if len(pt) > 0:
            pt[0].times += 1
            pt[0].save()
        else:
            pt = Poke.objects.create(poked_id=pokedt, poker_id=pokert, times=1)
    return redirect(reverse('pokes'))
# Create your views here.
