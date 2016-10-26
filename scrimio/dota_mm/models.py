from django.db import models
from player_acct.models import Player
import datetime

class DotaPlayer(models.Model):
	user_acct = models.ForeignKey(Player, related_name='dota_player')	# Scrimio User Account
	elo = models.IntegerField(default=500)								# User's Scrimio Rank

class Team(models.Model):
	name = models.SlugField(max_length=20) 								# Team Name
	description = models.TextField(max_length=200)
	players = models.ManyToManyField(DotaPlayer, related_name='teams') 	# All players on team
	elo = models.IntegerField(default=500) 								# Team over Scrimio Rank
	captain = models.ForeignKey(DotaPlayer, related_name="captain_of")
	
	def __unicode__(self):
		return self.name
		
class Match(models.Model):
	match_id = models.AutoField(primary_key=True, default=0)
	timestamp = datetime.datetime.now() 						# Time the match started
	winner = models.ForeignKey(Team)							# Winning team
	is_disputed = models.BooleanField(default=False) 			# Was the match disputed?
	teams = models.ManyToManyField(Team, related_name='matches')
	elo_modifier = models.IntegerField(default=25)				# How much elo changes for players (zero-sum game)