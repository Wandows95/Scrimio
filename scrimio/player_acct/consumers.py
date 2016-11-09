from .models import User, Player

from django.shortcuts import get_object_or_404

from channels import Group
from channels.sessions import channel_session
from channels.auth import channel_session_user_from_http, channel_session_user

@channel_session_user_from_http
def ws_login(message):
	user = get_object_or_404(User, username=message.user.username).player
	user.is_online = True
	user.save()

	# Join your own sub feed
	Group("feed-%s" % user.username).add(message.reply_channel)

	# Subscribe to friends list feed
	for player in user.friends.all():
		Group("feed-%s" % player.username).add(message.reply_channel)

@channel_session_user
def ws_status_update(message):
	data = json.loads(message['data'])
	status = data['status']
	username = data['username']

	# Broadcast user status
	Group("feed-%s" % username).send({'username':username, 'status': status})

@channel_session_user
def ws_logout(message):
	user = get_object_or_404(User, username=message.user.username).player
	user.is_online = False
	user.save()

	# Leave your own sub feed
	Group("feed-%s" % user.username).discard(message.reply_channel)

	# Unsubscribe from friends list feed
	for player in user.friends.all():
		Group("feed-%s" % player.username).discard(message.reply_channel)
