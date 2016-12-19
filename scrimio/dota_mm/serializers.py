'''
Rest API Definitions
'''
from .app_settings import GAME_NAME, TEAM_SIZE
from .models import Team, GamePlayer, Match, Status
from player_acct.models import Player
from player_acct.serializers import PlayerDataSerializer
from rest_framework import serializers
from rest_framework.exceptions import PermissionDenied
from player_acct import urls
from django.core import validators
from django.core.exceptions import ValidationError

class StatusDataSerializer(serializers.ModelSerializer):
	state = serializers.IntegerField(read_only=True)
	current_team = serializers.SlugField(source='current_team.name', default="")

	class Meta:
		model=Status
		fields=('state','current_team')

class GamePlayerSerializer(serializers.ModelSerializer):
	'''
	Serialize GamePlayer Model
	'''
	user_acct = PlayerDataSerializer(many=False, read_only=True)
	username = serializers.SlugField(source='user_acct.username')
	elo = serializers.IntegerField(read_only=True)
	status = StatusDataSerializer(read_only=True, many=False)

	class Meta:
		model=GamePlayer
		fields=('user_acct', 'elo', 'username', 'status',)

class TeamDataSerializer(serializers.ModelSerializer):
	'''
	Serializer for Team GET Actions
		- Players & Captain utilize nested serializers
	'''
	elo = serializers.IntegerField(read_only=True)
	players = GamePlayerSerializer(many=True, required=False)
	captain = GamePlayerSerializer(many=False, read_only=True)

	class Meta:
		model = Team
		fields = ('name', 'elo', 'description', 'captain', 'players',)

class TeamRosterSerializer(serializers.ModelSerializer):
	players = GamePlayerSerializer(many=True, required=False)
	captain = GamePlayerSerializer(many=False, read_only=True)

	class Meta:
		model = Team
		fields = ('players', 'captain',)

class TeamSerializer(serializers.ModelSerializer):
	'''
	Serializer for Team POST/PATCH Actions
		- Players & Captain linked by PK
		- create() auto-appoints captain to creating user
		- update() restricts permission to team captain
	'''
	elo = serializers.IntegerField(read_only=True)
	captain = serializers.PrimaryKeyRelatedField(queryset=GamePlayer.objects.all(), many=False, required=False)
	players = serializers.PrimaryKeyRelatedField(required=False, many=True, queryset=GamePlayer.objects.all())

	class Meta:
		model = Team
		fields = ('name', 'elo', 'description', 'captain', 'players',)

	def create(self, validated_data):
		# Protect from captain injection
		if validated_data.get('captain', None) != None:
			del validated_data['captain']

		team = Team(**validated_data)
		# Get the user's Game Account
		#print("CPT: %s " % )
		team.captain = getattr(self.context['request'].user.player, ("%s_player" % GAME_NAME)).get()
		team.save()
		return team

	def update(self, instance, validated_data):
		request_player = getattr(self.context['request'].user.player, ("%s_player" % GAME_NAME)).get()
		captain_req = validated_data.get('captain', None)
		players_req = validated_data.get('players', None)

		# Verify user is a team captain
		if request_player != instance.captain:
			raise PermissionDenied(detail="User is not captain")
			return

		# If API request is updating players
		if players_req is not None:
			# Enforce max team size
			if len(players_req) > TEAM_SIZE:
				raise serializers.ValidationError("Team size limited to %s" % TEAM_SIZE)
				return instance
			else:
				player_req_pk_list = [item.pk for item in players_req]
				# CURRENT captain can't be added as a player
				if instance.captain.pk in player_req_pk_list:
					raise serializers.ValidationError("User %s cannot be both player and captain" % instance.captain.pk)
					return instance
				# NEW captain can't be added as a player
				elif captain_req and captain_req.pk in player_req_pk_list:
					raise serializers.ValidationError("User %s cannot be both player and captain" % captain_req.pk)
					return instance

				# Remove duplicates
				instance.players = list(set(players_req))

		# If API request is updating captain
		if captain_req is not None:
			# Convert all current players to PKs
			player_pk_list = [item.pk for item in instance.players.all()]

			# If NEW captain is already a player
			if captain_req.pk in player_pk_list:
				# Remove NEW captain from players
				instance.players.remove(captain_req)
				if instance.captain.pk != captain_req.pk:
					# Demote OLD captain to Player
					instance.players.add(instance.captain)
			# Promote to captain
			instance.captain = captain_req

		# Update model fields & save
		instance.name = validated_data.get('name', instance.name)
		instance.description = validated_data.get('description', instance.description)
		instance.save()

		return instance

class MatchSerializer(serializers.ModelSerializer):
	match_id = serializers.IntegerField
	teams = TeamDataSerializer(read_only=True, many=True)

	class Meta:
		model = Match
		fields = ('match_id', 'teams',)

class GamePlayerTeamSerializer(serializers.ModelSerializer):
	'''
	Serializer for Player GET Actions
		- username is Django User's Username
		- teams user is on
		- captain_of teams listed here
		- teams & captain_of are mutually exclusive
	'''
	username = serializers.SlugField(source='user__username', read_only=True)
	teams = TeamDataSerializer(many=True)
	captain_of = TeamDataSerializer(many=True)
	
	class Meta:
		model = GamePlayer
		fields = ('username', 'teams', 'captain_of',)