'''
Set of pre-canned websocket actions
'''
from channels import Group, Channel

import json

def ws_send_team_queue_update(team_name, is_queued):
	Group("team-queue-%s" % team_name).send({"text":json.dumps({'action':'team-queue-update', 'is_queued': is_queued})})

def ws_send_player_queue_update(team_name, username, status_code):
	Group("team-queue-%s" % team_name).send({"text":json.dumps({'action':'team-queue-player-update', 'username': username, 'status': status_code})})

def ws_send_player_joined_match(team_name, match_id, username):
	'''
	Update team and match channels with new user join event
	'''
	Group("team-match-%s" % team_name).send({"text":json.dumps({'action':'team-match-player-join', 'username': username,})})
	Group("match-%s" % match_id).send({"text":json.dumps({'action':'team-match-player-join', 'username': username, 'team':team_name})})

def ws_send_player_match_redirect(match, game_player, reply_channel):
	# Check if player is in match before we allow redirect update
	if match.is_player_in_match(game_player):
		Channel(reply_channel).send({"text":json.dumps({'action':'player-match-redirect', 'match_id': match.match_id,})})
