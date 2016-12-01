'''
Top level Websocket routing.
'''
from channels import include, route

routes = [
	include("player_acct.routing.routes", path=r"^/user/sockets"),
]