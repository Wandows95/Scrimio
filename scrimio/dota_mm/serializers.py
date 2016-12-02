from .app_settings import GAME_NAME, TEAM_SIZE
from .models import Team, GamePlayer
from player_acct.models import Player
from player_acct.serializers import PlayerDataSerializer
from rest_framework import serializers
from rest_framework.exceptions import PermissionDenied
from player_acct import urls
from django.core import validators
from django.core.exceptions import ValidationError

# Serialize GamePlayer Model
class GamePlayerSerializer(serializers.ModelSerializer):
	user_acct = PlayerDataSerializer(many=False, read_only=True)
	username = serializers.SlugField(source='user_acct.username')
	elo = serializers.IntegerField(read_only=True)

	class Meta:
		model=GamePlayer
		fields=('user_acct', 'elo', 'username',)

# Serializer for Team GET Actions
# 	- Players & Captain utilize nested serializers
class TeamDataSerializer(serializers.ModelSerializer):
	elo = serializers.IntegerField(read_only=True)
	players = GamePlayerSerializer(many=True, required=False)
	captain = GamePlayerSerializer(many=False, read_only=True)

	class Meta:
		model = Team
		fields = ('name', 'elo', 'description', 'captain', 'players',)

# Serializer for Team POST/PATCH Actions
# 	- Players & Captain linked by PK
#	- create() auto-appoints captain to creating user
#	- update() restricts permission to team captain
class TeamSerializer(serializers.ModelSerializer):
	elo = serializers.IntegerField(read_only=True)
	captain = serializers.PrimaryKeyRelatedField(queryset=GamePlayer.objects.all(), many=False, required=False)
	players = serializers.PrimaryKeyRelatedField(queryset=GamePlayer.objects.all(), required=False, many=True)

	class Meta:
		model = Team
		fields = ('name', 'elo', 'description', 'captain', 'players',)

	def create(self, validated_data):
		# Protect from captain injection
		if validated_data.get('captain', None) != None:
			del validated_data['captain']

		team = Team(**validated_data)
		team.captain = getattr(self.context['request'].user.player, ("%s_player" % GAME_NAME)).get() # Get the user's Game Account
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

		if players_req is not None: # If API request is updating players
			if len(players_req) > TEAM_SIZE: # Enforce max team size
				raise serializers.ValidationError("Team size limited to %s" % TEAM_SIZE)
				return instance
			else:
				player_req_pk_list = [item.pk for item in players_req]

				if instance.captain.pk in player_req_pk_list: # CURRENT captain can't be added as a player
					raise serializers.ValidationError("User %s cannot be both player and captain" % instance.captain.pk)
					return instance
				elif captain_req and captain_req.pk in player_req_pk_list: # NEW captain can't be added as a player
					raise serializers.ValidationError("User %s cannot be both player and captain" % captain_req.pk)
					return instance

				instance.players = list(set(players_req)) # Remove duplicates

		if captain_req is not None: # If API request is updating captain
			player_pk_list = [item.pk for item in instance.players.all()] # Convert all current players to PKs

			if captain_req.pk in player_pk_list: 		# If NEW captain is already a player
				instance.players.remove(captain_req) 	# Remove NEW captain from players

				if instance.captain.pk != captain_req.pk:
					instance.players.add(instance.captain)	# Demote OLD captain to Player

			instance.captain = captain_req			# Promote to captain

		# Update model fields & save
		instance.name = validated_data.get('name', instance.name)
		instance.description = validated_data.get('description', instance.description)
		instance.save()

		return instance

# Serializer for Player GET Actions
#	- username is Django User's Username
#	- teams user is on
#	- captain_of teams listed here
#	- teams & captain_of are mutually exclusive
class PlayerTeamSerializer(serializers.ModelSerializer):
	username = serializers.SlugField(source='user__username', read_only=True)
	teams = TeamSerializer(many=True)
	captain_of = TeamSerializer(many=True)
	
	class Meta:
		model = GamePlayer
		fields = ('username', 'teams', 'captain_of',)