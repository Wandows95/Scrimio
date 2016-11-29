from .app_settings import GAME_NAME, TEAM_SIZE
from .models import Team, GamePlayer
from player_acct.models import Player
from player_acct.serializers import PlayerDataSerializer
from rest_framework import serializers
from rest_framework.exceptions import PermissionDenied
from player_acct import urls
from django.core import validators

class GamePlayerSerializer(serializers.ModelSerializer):
	user_acct = PlayerDataSerializer(many=False, read_only=True)
	elo = serializers.IntegerField(read_only=True)

	class Meta:
		model=GamePlayer
		fields=('user_acct', 'elo')


class TeamSerializer(serializers.ModelSerializer):
	elo = serializers.IntegerField(read_only=True)
	players = GamePlayerSerializer(many=True, read_only=True)
	captain = GamePlayerSerializer(many=False, read_only=True)
	#_add = serializers.Field(db_column='add_player', default={})
	#remove_player = serializers.SerializerMethodField()

	class Meta:
		model = Team
		fields = ('name', 'elo', 'description', 'captain', 'players', 'add',)

	def restore_object(self, attrs, instance=None):
		if instance is not None:
			instance.elo = attrs.get('elo', instance.elo)
			instance.players = attrs.get('players', instance.players)
			instance.captain = attrs.get('captain', instance.captain)

		add_player = attrs.get('add_player', None)
		remove_player = attrs.get('remove_player', None)
		
		if add_player is not None and self.validate_player_list(add_player):

		if remove_player is not None and self.validate_player_list(remove_player):


	def create(self, validated_data):
		if validated_data.get('captain', None) != None:
			del validated_data['captain'] # protect from captain injection

		team = Team(**validated_data)
		team.captain = getattr(self.context['request'].user.player, ("%s_player" % GAME_NAME)).get() # Get the user's Game Account
		team.save()
		return team

	def update(self, instance, validated_data):
		request_player = getattr(self.context['request'].user.player, ("%s_player" % GAME_NAME)).get()
		if request_player != instance.captain:
			raise PermissionDenied(detail="User is not captain")
		else:
			'''
			# If add_player field has a value and players cannot be added
			if 'add_player' in validated_data and add_player(validated_data['add_player'], instance):
				raise ValidationError(
				    _('Team size too large. Max Size:' %(size)),
				    code='TeamSizeTooLarge',
				    params={'size': TEAM_SIZE},)
			'''

			#print(validated_data)
			'''
			if 'remove_player' in validated_data and remove_player(validated_data['remove_player'], instance):
				raise ValidationError(
				    _('Attempting to remove too many players'),
				    code='TeamRemovedTooMany',)
			'''
			instance.name = validated_data.get('name', instance.name)
			instance.description = validated_data.get('description', instance.description)
			instance.captain = validated_data.get('captain', instance.captain)
			instance.save()

		return instance
	'''
	def add_player(player_pk_list, instance):
		player_pk_list = list(set(player_pk_list)) # Strip duplicates from the list
		# Subtract instance.player's primary keys from player_pk_list
		# Result ensures no duplicate players are added
		player_pk_list = [x for x in player_pk_list if x not in instance.players.values_list('id', flat=True)]

		# Ensure player isn't also added as a captain
		if instance.captain.pk in player_pk_list:
			player_pk_list.remove(instance.captain.pk)

		# Ensure not attempting to exceed team size
		if (instance.player.count() + player_pk_list.count()) > TEAM_SIZE - 1:
			return False # Unsuccessful transaction

		player_obj_list = GamePlayer.objects.in_bulk(player_pk_list) 	# Get player's objects
		instance.players.extend(player_obj_list)						# Add players to team

		return True

	def remove_player(player_pk_list, instance):
		player_pk_list = list(set(player_pk_list)) # Strip duplicates from the list
		# Strip invalid player pks from the list
		player_pk_list = [x for x in player_pk_list if x in instance.players.values_list('id', flat=True)]

		# Cannot remove Captain, he must be replaced
		if instance.captain.pk in player_pk_list:
			player_pk_list.remove(instance.captain.pk)

		# Ensure not attempting to delete too many
		if (instance.player.count() - player_pk_list.count()) < 0:
			return False # Unsuccessful transaction

		player_obj_list = GamePlayer.objects.in_bulk(player_pk_list) 	# Get player's objects

		for player in player_obj_list:
			instance.players.remove(player)						# Remove players

		return True
	'''

	# Manual Slug Field validation for player list
	def validate_player_list(list):
		for value in list:
			if not validators.validate_slug(value):
				 raise serializers.ValidationError("Not a slug")
				 return False

		return True

class TeamMemberSerializer(serializers.ModelSerializer):
	class Meta:
		model = Team
		fields = ('captain', 'players')

class PlayerTeamSerializer(serializers.HyperlinkedModelSerializer):
	teams = TeamSerializer(many=True)
	captain_of = TeamSerializer(many=True)
	
	class Meta:
		model = GamePlayer
		fields = ('teams', 'captain_of',)