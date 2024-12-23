from django.urls import path
from .views import (
    board_game_list,
    board_game_detail,
    register_view,
    login_view,
    toggle_favorite,
    profile_view,
    logout_view
)

urlpatterns = [
    path('', board_game_list, name='list'),
    path('<int:game_id>/', board_game_detail, name='detail'),
    path('<int:game_id>/toggle_favorite/', toggle_favorite, name='toggle_favorite'),

    path('register/', register_view, name='register'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('profile/', profile_view, name='profile'),
]