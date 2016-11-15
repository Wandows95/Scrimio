from .app_settings import GAME_NAME
from .models import Team, GamePlayer
from player_acct.models import Player
from player_acct.serializers import PlayerDataSerializer
from rest_framework import serializers

from player_acct import urls

class GamePlayerSerializer(serializers.ModelSerializer):
	user_acct = PlayerDataSerializer(many=False, read_only=True)

	class Meta:
		model=GamePlayer
		fields=('user_acct',)


class TeamSerializer(serializers.ModelSerializer):
	elo = serializers.IntegerField(read_only=True)
	players = GamePlayerSerializer(many=True, read_only=True)
	captain = GamePlayerSerializer(many=False, read_only=True)

	class Meta:
		model = Team
		fields = ('name', 'elo', 'description', 'captain', 'players',)

	def create(self, validated_data):
		team = Team(**validated_data)
		team.captain = getattr(self.context['request'].user.player, ("%s_player" % GAME_NAME)).get() # Get the user's Game Account
		team.save()
		return team

class PlayerTeamSerializer(serializers.HyperlinkedModelSerializer):
	teams = TeamSerializer(many=True)
	captain_of = TeamSerializer(many=True)
	
	class Meta:
		model = GamePlayer
		fields = ('teams', 'captain_of',)