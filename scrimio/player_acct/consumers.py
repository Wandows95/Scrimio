from .models import User

@channel_session_user_from_http
def ws_login(message):
	user = get_object_or_404(User, user=message.user)
	user.is_online = True
	user.save