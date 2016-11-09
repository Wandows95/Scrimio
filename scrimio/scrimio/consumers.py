from channels.sessions import channel_session
from channels.auth import channel_session_user_from_http

@channel_session_user_from_http
def ws_add(message):
    print("THIS WAS A TRIUMPH")

def ws_disconnect(message):
	print("GOODBYE HOMIE")