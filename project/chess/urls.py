from django.urls import path

from . import views
from .views import HotSeatView, IndexView

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    # to sa linki do rzeczy zwiazanych z grą lokalna
    path('game/selectmode/', views.modeselect, name='modeselect'),
    path('game/hotseat/', HotSeatView.as_view(), name='game'),
    path('game/aigame/', views.aigame, name='aigame'),
    # to sa linki do rzeczy z obsluga kont
    path('register', views.register_request, name='register'),
    path('login', views.login_request, name='login'),
    path('logout', views.logout_request, name='logout'),
    # to sa linki do rzeczy z gra online
    path('lobby/', views.onlinegamemodeselect, name='online lobby'),
    path('onlinegame/<str:room_name>', views.onlinegame, name='onlinegame'),
    path('users/<str:username>/', views.profile, name='profile'),
    path('page/<int:pageid>/', views.page, name='page')
]
