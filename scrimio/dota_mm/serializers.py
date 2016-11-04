from .models import Team, DotaPlayer
from player_acct.models import Player
from player_acct.serializers import PlayerSerializer
from rest_framework import serializers

from player_acct import urls

class DotaPlayerSerializer(serializers.ModelSerializer):
	user_acct = PlayerSerializer(many=False, read_only=True)

	class Meta:
		model=DotaPlayer
		fields=('user_acct',)


class TeamSerializer(serializers.HyperlinkedModelSerializer):
	elo = serializers.IntegerField(read_only=True)
	players = DotaPlayerSerializer(many=True)
	captain = DotaPlayerSerializer(many=False)
	
	class Meta:
		model = Team
		fields = ('name', 'elo', 'description', 'captain', 'players',)

class PlayerTeamSerializer(serializers.HyperlinkedModelSerializer):
	teams = TeamSerializer(many=True)
	captain_of = TeamSerializer(many=True)
	
	class Meta:
		model = DotaPlayer
		fields = ('teams', 'captain_of',)