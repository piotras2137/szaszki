from django.contrib.auth.models import User
from django.db import models
from django.db.models.deletion import CASCADE

# Create your models here.


class Invite(models.Model):
    invitor = models.ForeignKey(User, on_delete=CASCADE)
    choices = (
        ('black', 'Czarny'),
        ('white', 'Biały'),
        ('random', 'Losowy'),
    )
    invitor_color = models.CharField(
        "twój kolor", max_length=32, choices=choices)
    invite_date = models.DateTimeField(auto_now=True)
    status = models.CharField(default='active', max_length=32)

    def __str__(self):
        return str(self.pk) + ' ' + str(self.invite_date) + ' ' + str(self.invitor)


class Page(models.Model):
    title = models.CharField(max_length=64)
    content = models.TextField()

    def __str__(self):
        return str(self.pk) + ' ' + self.title


class AiGame(models.Model):
    pgn = models.TextField()
    result = models.TextField()
    player = models.ForeignKey(
        User, on_delete=CASCADE, blank=True, null=True)
    difficulty = models.CharField(max_length=32)
    playercolor = models.TextField()
    date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.pk) + " " + str(self.player) + " " + str(self.date)


class OnlineGame(models.Model):
    pgn = models.TextField()
    result = models.TextField()
    player1 = models.ForeignKey(
        User, on_delete=CASCADE, blank=True, null=True, related_name="playerwhite")
    player2 = models.ForeignKey(
        User, on_delete=CASCADE, blank=True, null=True, related_name="playerblack")
    date = models.DateTimeField(auto_now=True)
    invite = models.ForeignKey(
        Invite, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return str(self.pk) + " " + str(self.player1) + " " + str(self.player2) + " " + str(self.date)
