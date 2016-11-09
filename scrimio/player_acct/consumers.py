from .models import User

@channel_session_user_from_http
def ws_login(message):
	user = get_object_or_404(User, user=message.user)
	user.is_online = True
	user.save()

	# Join your own sub feed
	Group("feed-%s" % user.username).add(message.reply_channel)

	# Subscribe to friends list feed
	for player in user.friends.all():
		Group("feed-%s" % player.username).add(message.reply_channel)

@channel_session
def ws_status_update(message):
	data = json.loads(message['data'])
	status = data['status']
	username = data['username']

	# Broadcast user status
	Group("feed-%s" % username).send({'username':username, 'status': status})

@channel_session
def ws_logout(message):
	user = get_object_or_404(User, user=message.user)
	user.is_online = False
	user.save()

	# Leave your own sub feed
	Group("feed-%s" % user.username).discard(message.reply_channel)

	# Unsubscribe from friends list feed
	for player in user.friends.all():
		Group("feed-%s" % player.username).discard(message.reply_channel)
