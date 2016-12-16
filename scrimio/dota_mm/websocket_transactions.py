'''
Set of pre-canned websocket actions
'''
from channels import Group, Channel

def ws_send_team_queue_update(team_name, is_queued):
	Group("team-queue-%s" % team_name).send({"text":json.dumps({'action':'team-queue-update', 'is_queued': is_queued})})

def ws_send_player_queue_update(team_name, username, is_queued):
	Group("team-queue-%s" % team_name).send({"text":json.dumps({'action':'team-queue-player-update', 'username': username, 'is_queued': is_queued})})