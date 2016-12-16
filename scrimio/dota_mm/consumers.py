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
from .models import Team, GamePlayer, Status, Match
from .matchmaking import mm_can_team_queue, mm_find_match
from .status import MUTEX_STATUS, OFFLINE, ONLINE, READY, IN_QUEUE
from .skill import skill_calculate_match

import json

# websocket.connect
@channel_session
@channel_session_user_from_http
def ws_queue_join(message, team_name):
	#result = skill_calculate_match({'User1':[220,0.83], 'User2':[215,0.81], 'User3':[205,0.79]}, {'User4':[220,0.83], 'User5':[215,0.81], 'User6':[205,0.79]}, 1)
	'''
	Checks if user's status is not mutually exclusive
	Handles the conditions of a user ready up:
		- Offline -> Ready
		- Ready -> In-Queue
		- Ready -> 404
	'''
	team = get_object_or_404(Team, name=team_name)
	game_player = get_game_player(message.user)
	chan_session = message.channel_session
	mm_status = game_player.status
	
	# Ensure GamePlayer exists
	# Check player Authentication #
	# Need to verify game account #

	# Ensure this user isn't already busy and belongs on the team they're attempting to queue with
	if team.is_game_player_on_team(game_player) and game_player.is_busy() is False:
		# Update player's selected team
		game_player.status.current_team = team
		# Save pk to session
		message.channel_session['mm_game_player_pk'] = game_player.pk
		# Update user's current status state
		mm_status.state = READY if mm_can_team_queue(team.captain, team.players) is not True else IN_QUEUE
		mm_status.current_team = team

		# Flag team is queued if user has triggered queue
		if mm_status.state == IN_QUEUE:
			mm_status.current_team.is_queued = True
			mm_status.current_team.save(update_fields=['is_queued'])
			print("TEAM QUEUED? %s" % mm_status.current_team.is_queued)

		# Update GamePlayer's Status in DB
		mm_status.save(update_fields=['state', 'current_team'])
		# Subscribe to team's feed
		Group("team-%s" % team_name).add(message.reply_channel)

		'''
		# Tell users in team feed ready
		if mm_status.state != IN_QUEUE or mm_status.current_team.is_queued == False:
			Group("team-%s" % team_name).send({"text":json.dumps({'player_status': mm_status.state, 'user':message.user.username})})
		# If mm_status and current_team's IN_QUEUE status are mismatched
		elif (mm_status.state == IN_QUEUE) != mm_status.current_team.is_queued:
			pass
		elif mm_status.state == IN_QUEUE and mm_status.current_team.is_queued == True:
			new_match_id = mm_find_match(mm_status.current_team)
			Group("team-%s" % team_name).send({"text":json.dumps({'player_status': mm_status.state, 'user':message.user.username, 'match_id':new_match_id, 'team_queued':mm_status.current_team.name})})
		'''
		print("%s readied up on %s!" % (game_player.user_acct.username, team.name))
	else:
		return False

@channel_session
@channel_session_user
def ws_queue_disconnect(message, team_name):
	'''
	Resets matchmaking data on disconnect:
		- channel_session['mm_game_player_pk']
		- Status.state
		- Status.current_team
	'''
	game_player = get_game_player(message.user)
	if game_player is not None:
		mm_status = game_player.status
		if game_player.status.current_team is not None and game_player.status.current_team.is_queued:
			game_player.status.current_team.is_queued=False
		print("%s has left %s's channel" % (message.user.player.username, mm_status.current_team.name))
		# Flag to users that you're offline and leave
		Group("team-queue-%s" % mm_status.current_team.name).send({"text":json.dumps({'status': OFFLINE, 'user':message.user.username})})
		Group("team-queue-%s" % mm_status.current_team.name).discard(message.reply_channel)
		# Reset matchmaking session data
		if mm_status.state == IN_QUEUE:
			mm_status.current_team.is_queued =False
			mm_status.current_team.save(update_fields=['is_queued'])
			print("IS TEAM QUEUED? %s" % mm_status.current_team.is_queued)
		
		mm_status.state = OFFLINE
		mm_status.current_team = None
		mm_status.save(update_fields=['state', 'current_team'])

@channel_session
@channel_session_user
def ws_match_join(message, match_id):
	pass

@channel_session
@channel_session_user
def ws_match_relay(message, match_id):
	pass

@channel_session
@channel_session_user
def ws_match_disconnect(message, match_id):
	pass
