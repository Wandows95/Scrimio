'''
Set of pre-canned database transactions
'''
from player_acct.models import Player
from .models import Team, GamePlayer
from django.shortcuts import get_object_or_404
from .app_settings import GAME_NAME

# Extracts user's GamePlayer from session user
def get_game_player(session_user):
	player = get_object_or_404(Player, user=session_user)
	game_player = getattr(player, ("%s_player" % GAME_NAME))
	return game_player.all().first()
