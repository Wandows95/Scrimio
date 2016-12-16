'''
Websocket-specific routing
'''
from channels import route, include
from . import consumers

from .app_settings import GAME_NAME

queue_routing = [
    route("websocket.connect", consumers.ws_queue_join, path=r"^/(?P<team_name>[-\w]+)/"),
	route("websocket.disconnect", consumers.ws_queue_disconnect, path=r"^/(?P<team_name>[-\w]+)/"),
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