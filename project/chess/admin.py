from django.contrib import admin
from .models import Invite, Page, AiGame, OnlineGame
# Register your models here.
admin.site.register(Invite)
admin.site.register(Page)
admin.site.register(AiGame)
admin.site.register(OnlineGame)
