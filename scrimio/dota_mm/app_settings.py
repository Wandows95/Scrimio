"""
App specific settings for Matchmaking app

Used to generalize aspects of the Matchmaker for easy deployment in other games
"""

GAME_NAME = "dota"					# Used to specify Game Name for generated routes
TEAM_SIZE = 5 						# Number of players on a team
APP_NAME = ("%s_mm" % GAME_NAME) 	# Generated name of app