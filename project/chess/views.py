from webbrowser import get
from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from .forms import NewUserForm, Gamemodeselectionform
from django.contrib.auth import login, authenticate, logout, get_user_model
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from django import forms
import random
from .forms import InviteCreateForm, InvitationJoinForm, AiGameSaveForm, OnlineGameSaveForm
from django.contrib.auth.models import User
from .models import Invite, AiGame, OnlineGame, Page

from django.views import View
from django.views.generic import TemplateView, DetailView

from datetime import timedelta
from django.db.models.functions import Now


class IndexView(TemplateView):
    template_name = 'index.html'


class HotSeatView(TemplateView):
    template_name = 'game/game.html'


def aigame(request):

    old_post = request.session.get('_post_data')
    print(old_post)
    color = old_post['color']
    difficulty = old_post['dificulty']
    print(color)
    print(difficulty)
    if color not in ['black', 'white']:
        color = random.choice(['black', 'white'])

    form = AiGameSaveForm(request.POST)
    context = {
        'color': color,
        'difficulty': difficulty,
        'form': form,
    }
    if request.method == 'POST':
        if form.is_valid():
            x = form.save(commit=False)
            if request.user.pk:
                if x.difficulty == '0':
                    x.difficulty = "łatwy"
                elif x.difficulty == '1':
                    x.difficulty = 'średni'
                elif x.difficulty == '2':
                    x.difficulty = 'trudny'
                x.player = User.objects.get(pk=request.user.pk)
                x.save()
                return redirect('/game/selectmode/')

    return render(request, 'game/aigame.html', context)


def modeselect(request):
    form = Gamemodeselectionform(request.POST)

    if request.method == 'POST':
        if form.is_valid():
            request.session['_post_data'] = request.POST
            return redirect('/game/aigame')

    return render(request, 'modeselect.html', {'form': form})


def onlinegamemodeselect(request):
    form = InviteCreateForm(request.POST)
    joinform = InvitationJoinForm(request.POST)
    context = {
        'form': form,
        'joinform': joinform,
    }

    if form.is_valid():
        x = form.save(commit=False)
        if x.invitor_color not in ['black', 'white']:
            x.invitor_color = random.choice(['black', 'white'])

        try:
            print(request.user)
            x.invitor = User.objects.get(pk=request.user.pk)
            x.save()
            msgstr = 'stworzono zaproszenie , numer zaproszenia ' + str(x.pk)
            print(msgstr)
            messages.success(request, message=msgstr)
            return redirect('/onlinegame/'+str(x.pk))
        except:
            messages.error(
                request, 'niezalogowani użytkownicy nie mogą tworzyć zaproszeń do gry')

    if joinform.is_valid():
        codefield = request.POST['codefield']
        try:
            x = Invite.objects.get(pk=codefield)
            if x.status == 'used':
                messages.error(
                    request, 'kod zaproszenia został już wykorzystany lub jest już nieaktywny')
            else:
                messages.success(request, 'dołączono do gry')
                return redirect('/onlinegame/' + codefield)
        except Invite.DoesNotExist:
            messages.error(
                request, 'nie znaleziono podanego zaproszenia')
            return redirect('/lobby/')

    return render(request, 'onlinemodeselect.html', context=context)


# wszystkie rzeczy do obslugi usera

def register_request(request):
    if request.method == 'POST':
        form = NewUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Rejestracja udana.')
            return redirect('/')
        messages.error(
            request, 'Rejestracja nieudana, podano nieprawidłowe informacje.')
    form = NewUserForm()
    return render(request=request, template_name='account/register.html', context={'register_form': form})


def login_request(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.info(request, f'Zalogowano jako {username}.')
                return redirect('/')
            else:
                messages.error(request, 'Niewłaściwy login lub hasło.')
        else:
            messages.error(request, 'Niewłaściwy login lub hasło.')
    form = AuthenticationForm()
    return render(request=request, template_name='account/login.html', context={'login_form': form})


def logout_request(request):
    logout(request)
    messages.info(request, 'Pomyślnie wylogowano')
    return redirect('index')


# to jest testowe, potem to wywal ziomeczku

def room(request, room_name):
    return render(request, 'room.html', {'room_name': room_name})


def onlinepassthrough(request, room_name):
    return render(request, 'game/opt.html', {'room_name': room_name})


def onlinegame(request, room_name):
    invites = Invite.objects.filter(invite_date__lte=Now()-timedelta(hours=2))
    for invite in invites:
        if invite.status == "active":
            invite.status = "used"
            invite.save()

    if not room_name.isdigit():
        messages.error(request, 'podany kod zawiera niewłaściwe znaki')
        return redirect('/lobby/')
    invite = Invite.objects.get(pk=room_name)
    if invite.status == "used":
        messages.error(
            request, "zaproszenie zostało już wykorzystane lub jest już przedawnione, nie można go więcej używać")
        return redirect('/lobby/')
    usr = request.user
    form = OnlineGameSaveForm(request.POST)
    context = {
        'color': 0,
        'room_name': room_name,
        'invite': invite,
        'usr': usr.username,
        'form': form,
    }

    if request.method == 'POST':
        if form.is_valid():
            x = form.save(commit=False)
            x.invite = Invite.objects.get(pk=room_name)
            z = x.invite
            print(x.result)
            if z.status != 'used':
                z.status = 'used'
                z.save()
                x.save()
                return redirect('/lobby/')
            else:
                return redirect('/lobby/')

    return render(request, 'game/onlinegame.html', context)


def profile(request, username):
    x = get_user_model()
    user = x.objects.get(username=username)
    aigames = AiGame.objects.filter(player=user).order_by('-pk')[:5]
    og1 = OnlineGame.objects.filter(player1=user)
    og2 = OnlineGame.objects.filter(player2=user)
    onlinegames = og1 | og2
    onlinegames = onlinegames.order_by('-pk')[:5]
    context = {'usr': user, 'aigames': aigames, 'onlinegames': onlinegames}
    return render(request, 'profile.html', context)


def page(request, pageid):
    x = Page.objects.get(pk=pageid)
    context = {
        'page': x,
    }
    return render(request, "page.html", context=context)
