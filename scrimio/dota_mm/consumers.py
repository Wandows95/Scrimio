from player_acct.models import User
from .models import Team

from channels import Group
from channels.sessions import channel_session
from channels.auth import channel_session_user_from_http

# websocket.connect
@channel_session_user_from_http
def ws_join(message, team_name):
	# Ensure user exists and is authenticated
	user = get_object_or_404(User, user=message.user)
	# Ensure team exists
	team = get_object_or_404(Team, name=team_name)
	
	if !team.players.exists(user.dota_player): # 404 if player is not on team
		raise Http404("You are not in this team")
	elif user.steam_id == 'null'# 404 if player has no STEAM_ID
		raise Http404("You don't have a steam id associated with this account")
	else:
		message.channel_session['team'] = team_name
		Group("team-%s" % team_name).add(message.reply_channel) # subscribe to team

@channel_session
def ws_status(message):
	data = json.loads(message['data'])
	status = data['status']
	user = data['user']
	# Broadcast user status
	
	Group("team-%s" % message.channel_session['team']).send({'status': status, 'user':user})

@channel_session
def ws_disconnect(message, team_name):
	Group("team-%s" % team_name).discard(message.reply_channel)