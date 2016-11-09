from channels import include, route
from . import consumers

scrimio_routes = [
	route("websocket.connect", consumers.ws_add, path=r"^/test"),
	route("websocket.disconnect", consumers.ws_disconnect, path=r"^/test"),
]

routes = [
	include("player_acct.routing.routes", path=r"^/user/sockets"),
	include(scrimio_routes, path=r"^/scrimio/sockets"),
]