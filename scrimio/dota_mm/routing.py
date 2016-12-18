'''
Websocket-specific routing
'''
from channels import route, include
from . import consumers

from .app_settings import GAME_NAME

queue_routing = [
    route("websocket.connect", consumers.ws_team_queue_player_connect, path=r"^/(?P<team_name>[-\w]+)/"),
    route("websocket.receive", consumers.ws_team_queue_player_toggle_status, path=r"^/(?P<team_name>[-\w]+)/"),
	route("websocket.disconnect", consumers.ws_team_queue_player_disconnect, path=r"^/(?P<team_name>[-\w]+)/"),
]

match_routing = [
	route("websocket.connect", consumers.ws_match_join, path=r"^/(?P<match_id>[0-9]+)/"),
	route("websocket.receive", consumers.ws_match_relay, path=r"^/(?P<match_id>[0-9]+)/"),
	route("websocket.disconnect", consumers.ws_match_disconnect, path=r"^/(?P<match_id>[0-9]+)/"),
]

routes = [
    include(queue_routing, path=r"^/status"),
    include(match_routing, path=r"^/match"),
]