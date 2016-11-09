from channels import route
from . import consumers

routes = [
	route("websocket.connect", consumers.ws_login, path=r"^/login"),
	route("websocket.disconnect", consumers.ws_logout, path=r"^/login"),
]