'''
Channel/Websocket message consumer method definitions for Matchmaker
'''
from player_acct.models import Player
from django.shortcuts import get_object_or_404
from channels import Group, Channel
from channels.sessions import channel_session
from channels.auth import channel_session_user_from_http, channel_session_user

from .app_settings import GAME_NAME
from .transactions import get_game_player
from .websocket_transactions import ws_send_player_queue_update, ws_send_team_queue_update
from .models import Team, GamePlayer, Status, Match
from .matchmaking import mm_can_team_queue, mm_find_match, mm_can_match_user_connect
from .status import status_is_transition_allowed, OFFLINE, ONLINE, READY, IN_QUEUE
from .skill import skill_calculate_match

import json

# websocket.connect
@channel_session
@channel_session_user_from_http
def ws_team_queue_player_connect(message, team_name):
	team = get_object_or_404(Team, name=team_name)
	chan_session = message.channel_session
	game_player = get_game_player(message.user, chan_session)
	mm_status = game_player.status
	
	# Ensure GamePlayer exists
	# Check player Authentication #
	# Need to verify game account #
	print(mm_status.current_team)
	print(team.is_game_player_on_team(game_player))
	print(mm_status.is_busy())
	# User is on team and NOT in a MUTEX_STATUS with another team
	if mm_status.current_team == None and team.is_game_player_on_team(game_player) and mm_status.is_busy() is False:
		mm_status.state = ONLINE
		mm_status.save(update_fields=['state'])
		# Announce to team's queue channel of your status
		Group("team-queue-%s" % team_name).add(message.reply_channel)
		print("USER ONLINE")
		ws_send_player_queue_update(team.name, message.user.player.username, mm_status.state)


@channel_session
@channel_session_user
def ws_team_queue_player_toggle_status(message, team_name):

	team = get_object_or_404(Team, name=team_name)
	chan_session = message.channel_session
	game_player = get_game_player(message.user, chan_session)
	mm_status = game_player.status

	print(mm_status.state)

	if team.is_game_player_on_team(game_player):
		# Online -> Ready
		if mm_status.state == ONLINE and mm_status.current_team == None:
			# Tie user to team and ready up
			mm_status.current_team = team
			mm_status.state = READY
			mm_status.save(update_fields=['current_team', 'state'])

		# Ready -> Online
		elif mm_status.state == READY and mm_status.current_team != None:
			# Relinquish user from team
			mm_status.current_team = None
			mm_status.state = ONLINE
			mm_status.save(update_fields=['current_team', 'state'])

	# In_Queue -> Online
	elif mm_status.state == IN_QUEUE and mm_status.current_team.is_queued and mm_status.current_team == team:
		# Degrade team status
		for player in team.players.all():
			if player.status.state == IN_QUEUE:
				player.status.state = READY
				player.status.state.save(update_fields=['state'])

		# Update team's queue status and announce
		team.is_queued = False
		team.save(update_fields=['is_queued'])
		ws_send_team_queue_update(mm_status.current_team.name, False)
		mm_status.current_team = None
		# Degrade user's status 
		mm_status.state = ONLINE
		mm_status.save(update_fields=['current_team', 'state'])

	# Announce player statuses update
	ws_send_player_queue_update(team.name, message.user.player.username, mm_status.state)

@channel_session
@channel_session_user
def ws_team_queue_player_disconnect(message, team_name):
	team = get_object_or_404(Team, name=team_name)
	chan_session = message.channel_session
	game_player = get_game_player(message.user, chan_session)
	mm_status = game_player.status

	if team.is_game_player_on_team(game_player):
		if mm_status.state == IN_QUEUE and mm_status.current_team == team:
			
			# Degrade team status
			for player in team.players.all():
				if player.status.state == IN_QUEUE:
					player.status.state = READY
					player.status.state.save(update_fields=['state'])
			# Update team's queue status and announce
			team.is_queued = False
			team.save(update_fields=['is_queued'])
			ws_send_team_queue_update(mm_status.current_team.name, False)

		mm_status.current_team = None
		mm_status.state = OFFLINE
		mm_status.save(update_fields=['state', 'current_team'])

		# Alert team of update
		ws_send_player_queue_update(team.name, message.user.player.username, mm_status.state)
		Group("team-queue-%s" % team_name).discard(message.reply_channel)

@channel_session
@channel_session_user
def ws_match_join(message, match_id):
	game_player = GamePlayer.objects.get(pk=message.channel_session['mm_game_player_pk']) if 'mm_game_player_pk' in message.channel_session.keys() else get_game_player(message.user)
	match = Match.objects.get(match_id=match_id)
	game_player_team = None

	if game_player is not None and match is not None and mm_can_match_user_connect(match, game_player):
		game_player_team = game_player.status.current_team.all()

		# Add user to team and match channel
		Group("team-match-%s" % (game_player_team.name)).add(message.reply_channel)
		Group("match-%s" % (match_id)).add(message.reply_channel)

		# Add user to team and match channel
		ws_send_player_joined_match(game_player_team.name, match.match_id, user_acct.player.username)
		# Ensure user gets redirect notice incase this connect occurs outside of match webpage
		ws_send_player_match_redirect(match, game_player, message.reply_channel)

@channel_session
@channel_session_user
def ws_match_relay(message, match_id):
	pass

@channel_session
@channel_session_user
def ws_match_disconnect(message, match_id):
	pass
