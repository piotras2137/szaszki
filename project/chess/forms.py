from django import forms
from django.contrib.auth.forms import UserChangeForm, UserCreationForm
from django.contrib.auth.models import User
from django.forms import fields

from .models import Invite, AiGame, OnlineGame


class NewUserChangeForm(UserChangeForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name')


class NewUserForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

    def save(self, commit=True):
        user = super(NewUserForm, self).save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user


class Gamemodeselectionform(forms.Form):
    difficulychoices = [(0, 'Łatwy'), (1, 'Średni'), (2, 'Trudny')]
    colorchoices = [('black', 'Czarny'), ('white', 'Biały'),
                    ('random', 'Losowo')]
    dificulty = forms.CharField(label='poziom trudności', widget=forms.Select(
        choices=difficulychoices), required=False)
    color = forms.CharField(
        label='kolor', widget=forms.Select(choices=colorchoices))


class InviteCreateForm(forms.ModelForm):

    class Meta:
        model = Invite
        fields = [
            'invitor_color',
        ]


class InvitationJoinForm(forms.Form):
    codefield = forms.CharField(label='podaj kod gry')


class AiGameSaveForm(forms.ModelForm):

    class Meta:
        model = AiGame
        fields = [
            'pgn',
            'result',
            'player',
            'difficulty',
            'playercolor',
        ]


class OnlineGameSaveForm(forms.ModelForm):

    class Meta:
        model = OnlineGame
        fields = [
            'pgn',
            'result',
            'player1',
            'player2',
            'invite',
        ]
