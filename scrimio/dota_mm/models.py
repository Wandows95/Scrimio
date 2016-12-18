from django.db import models
from django.dispatch import receiver
from django.db.models.signals import post_save
from player_acct.models import Player
import datetime
from .app_settings import GAME_NAME, TEAM_SIZE, ELO_MODIFIER
from django.core.exceptions import ValidationError

from .websocket_transactions import ws_send_team_queue_update, ws_send_player_queue_update
from .status import GAMEPLAYER_STATUS_CHOICES, MUTEX_STATUS, OFFLINE, READY, IN_QUEUE

class GamePlayer(models.Model):
	'''
	Player specific to game

	Local Fields:
	----------------
	- user_acct: Link to Scrimio specific user account
	- elo: User's current game skill ranking

	Related Fields:
	----------------
	- current_team: Link to Team user is currently involved with live
	- teams: List of teams user is enrolld on
	- captain_of: List of teams user is in charge of

	'''
	user_acct = models.ForeignKey(Player, related_name=('%s_player' % (GAME_NAME,)))
	elo = models.IntegerField(default=500)

	# Automatically create a game specific player for the new account
	@receiver(post_save, sender=Player)
	def acct_player_post_save(sender, instance, created, *args, **kwargs):
		if created:
			game_player = GamePlayer.objects.create(user_acct=instance)

	def is_busy(self):
		return self.status.is_busy()

	def is_ready(self):
		return self.status.state is READY

	def register_win(self):
		self.elo = self.elo + ELO_MODIFIER
		self.save()

	def register_loss(self):
		self.elo = self.elo - ELO_MODIFIER
		self.save()

class Team(models.Model):
	'''
	Game specific Team
	'''
	__diff_is_queued = None

	name = models.SlugField(max_length=20)
	description = models.TextField(max_length=200)
	players = models.ManyToManyField(GamePlayer, related_name='teams')
	# Team Scrimio Rank
	elo = models.IntegerField(default=500)
	captain = models.ForeignKey(GamePlayer, related_name="captain_of")
	is_queued = models.BooleanField(default=False)
	
	def __unicode__(self):
		return self.name
		
	def clean(self, *args, **kwargs):
		'''
		Check team size
		'''
		#related_objs = self.players

		#if related_objs:
		#	if len(related_objs) > TEAM_SIZE:
		#		raise ValidationError('Maximum team size is %s players.' % TEAM_SIZE)

		super(Team, self).clean(*args, **kwargs)

	def save(self, *args, **kwargs):
		'''
		# Check if queue status has been updated
		if self.is_queued != self.__diff_is_queued:
			# Send queue update realtime notification
			ws_send_team_queue_update(self.name, self.is_queued)
			# Cache new value
			self.__diff_is_queued = self.is_queued
		'''
		# Invoke all validation every save
		self.full_clean()
		super(Team, self).save(*args, **kwargs)

	def is_game_player_on_team(self, player):
		return player in self.players.all() or player.pk == self.captain.pk

class Status(models.Model):

	__diff_state = None

	player = models.OneToOneField(GamePlayer, on_delete=models.CASCADE, related_name="status", primary_key=True)
	state = models.IntegerField(default=OFFLINE, choices=GAMEPLAYER_STATUS_CHOICES)
	current_team = models.ForeignKey(Team, related_name="reserved_players", null=True, blank=True, default=None)

	# Automatically create a game specific player for the new account
	@receiver(post_save, sender=GamePlayer)
	def game_player_post_save(sender, instance, created, *args, **kwargs):
		if created:
			player_status = Status.objects.create(player=instance)

	def is_busy(self):
		return self.state in MUTEX_STATUS

	'''
	def clean(self, *args, **kwargs):
		# Check if state transition is allowed
		if self.__diff_state != None and self.__diff_state != self.state:
			if self.__diff_state in MUTEX_STATUS and self.state in MUTEX_STATUS:
				raise ValidationError("Cannot transition between %s and %s" % (self.__diff_state, self.state,))
			
		super(Match, self).clean(*args, **kwargs)


	def save(self, *args, **kwargs):
		# Invoke all validation every save
		self.full_clean()

		# Check if queue status has been updated
		if self.state != self.__diff_state:
			# IN_QUEUE -> state
			if self.__diff_state == IN_QUEUE:
				ws_send_player_queue_update(self.current_team.name, self.player.username, False)
			# state -> IN_QUEUE
			elif self.state == IN_QUEUE:
				ws_send_player_queue_update(self.current_team.name, self.player.username, True)
			
			self.__diff_is_queued = self.is_queued

		super(Team, self).save(*args, **kwargs)
	'''


class Match(models.Model):
	'''
	Single instance of Game's match
	'''
	match_id = models.AutoField(primary_key=True)
	# Time the match started
	start_timestamp = models.DateTimeField(default=datetime.datetime.now(), blank=True)
	# Time the match ended
	end_timestamp = models.DateTimeField(default=None, blank=True)
	# Winning team
	winner = models.ForeignKey(Team, null=True, blank=True, default=None)
	# Was the match disputed?
	is_disputed = models.BooleanField(default=False)
	teams = models.ManyToManyField(Team, related_name='matches')
	# How much elo changes for players (zero-sum game)		
	elo_modifier = models.IntegerField(default=25)

	# Check if user exists in match
	def is_player_in_match(self, game_player):
		# Is player on a team within this match?
		for team in self.teams.all():
			if team.is_game_player_on_team(game_player):
				return True
		return False

	def clean(self, *args, **kwargs):
	 	# Ensure end time is after start time
		if end_timestamp != None and start_timestamp > end_timestamp:
			raise ValidationError("A match cannot start after it ends!")
		super(Match, self).clean(*args, **kwargs)

	def save(self, *args, **kwargs):
		# Invoke all validation every save
		self.full_clean()
		super(Match, self).save(*args, **kwargs)