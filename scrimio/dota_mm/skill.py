'''
Skill ranking implementation for Matchmaking

* ``skill_calculate_match`` for actual elo adjustment
* ``skill_is_match_fair`` for determining potential fairness

'''
from trueskill import Rating, quality, rate
from collections import OrderedDict

def skill_calculate_match(team_1_elo, team_2_elo, team_num_won):
	'''
	Takes 2 lists of elos and a match outcome and computes elo
		- team_x_elo = {'User1':[mu,sigma], 'User2':[mu,sigma], 'User3':[mu,sigma]}
		- team_num_won = 1 or 2
	''' 
	# Ensure order is enforced before stripping values from keys
	team_1_elo_sort = OrderedDict(sorted(team_1_elo.items(), key=lambda t: t[1]))
	team_2_elo_sort = OrderedDict(sorted(team_2_elo.items(), key=lambda t: t[1]))
	# Holds stripped ratings
	team_1_ratings = skill_to_rating_array(team_1_elo_sort)
	team_2_ratings = skill_to_rating_array(team_2_elo_sort)
	# Lower number is winner
	result_mask = [1,0] if team_num_won == 2 else [0,1]
	# Calculate new elos based on result_mask
	results = rate([team_1_ratings, team_2_ratings], result_mask)
	# Build new skill result
	team_1_result = skill_build_new_team_elo(team_1_elo_sort, results)
	team_2_result = skill_build_new_team_elo(team_2_elo_sort, results, team_num=1)
	
	return({'team_1_result': team_1_result, 'team_2_result':team_2_result})

def skill_is_match_fair(team_1_elo, team_2_elo, fairness_threshold):
	# Ensure order is enforced before stripping values from keys
	team_1_elo_sort = OrderedDict(sorted(team_1_elo.items(), key=lambda t: t[1]))
	team_2_elo_sort = OrderedDict(sorted(team_2_elo.items(), key=lambda t: t[1]))
	# Holds stripped ratings
	team_1_ratings = skill_to_rating_array(team_1_elo_sort)
	team_2_ratings = skill_to_rating_array(team_2_elo_sort)

	fairness = quality([team_1_ratings, team_2_ratings])
	
	if fairness >= fairness_threshold:
		return True

	return False

def skill_to_rating_array(sorted_elo_dict):
	'''
	Strips values from dictionary keys 'mu' & 'sigma'.
	Stripping preserves order.
	Returns array of stripped values 
	'''
	rating_array = []

	for key, item in sorted_elo_dict.items():
		rating_array.append(Rating(mu=item[0], sigma=item[1]))

	return rating_array

def skill_build_new_team_elo(original_elo_dict, results, team_num=0):
	'''
	Combine the resulting mu and sigma (elo) values into computed_elo dictionary
	Recreates original_elo_dict with updated mu & sigma values
	'''
	computed_elo = {}

	i = 0
	for key, value in original_elo_dict.items():
		computed_elo[key] = [int(results[team_num][i].mu), results[team_num][i].sigma]
		i = i + 1

	return computed_elo