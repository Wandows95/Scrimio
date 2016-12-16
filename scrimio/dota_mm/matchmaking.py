from .models import Match
'''
Contains the rules and constraints for matchmaker
'''

def mm_find_match(team_1, team_2=None):
	'''
	Returns a new match, adding the team(s) to the match
	'''
	new_match = Match.objects.create()
	new_match.save()
	new_match.teams.add(team_1)

	if team_2 is not None:
		new_match.teams.add(team_2)

	new_match.save()

	return new_match.match_id

def mm_can_team_queue(captain, players):
	#num_not_ready = 0
	for player in players.all():
		if player.is_ready() == False:
			#num_not_ready = num_not_ready + 1
			#if num_not_ready > 1:
			return False

	if captain.is_ready() == False:
		#num_not_ready = num_not_ready + 1
		return False

	return num_not_ready < 2

def mm_can_match_user_reconnect(match, game_player):
	# Check if match has ended
	if end_timestamp == None:
		return False
	# Is player on a team within this match?
	for team in match.teams.all():
		if team.is_game_player_on_team(game_player):
			return True

	return False