"""
App specific settings for Matchmaking app

Used to generalize aspects of the Matchmaker for easy deployment in other games
"""

GAME_NAME = "dota"					# Used to specify Game Name for generated routes
TEAM_SIZE = 5 						# Number of players on a team
APP_NAME = ("%s_mm" % GAME_NAME) 	# Generated name of app

# Ranking Settings
ELO_RANK_INCREMENT=500				# How ranks are sequestered
ELO_MODIFIER = 25					# How elo is adjusted
ELO_MATCH_FAIRNESS_THRESHOLD = 0.42 # Lowest match fairness is 42% change of draw

# Matchmaking Settings
