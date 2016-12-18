'''
Set of pre-canned database transactions
'''
from player_acct.models import Player
from .models import Team, GamePlayer
from django.shortcuts import get_object_or_404
from .app_settings import GAME_NAME

# Extracts user's GamePlayer from session user
def get_game_player(session_user, channel_session=None):

	# Extract pk from session if exists
	if channel_session is not None:
		if 'mm_game_player_pk' in channel_session.keys():
			return GamePlayer.objects.get(pk=channel_session['mm_game_player_pk'])

	player = get_object_or_404(Player, user=session_user)
	game_player = getattr(player, ("%s_player" % GAME_NAME))
	return game_player.all().first()
