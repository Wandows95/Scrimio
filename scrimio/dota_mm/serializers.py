from .models import Team, DotaPlayer
from player_acct.models import Player
from rest_framework import serializers

class TeamSerializer(serializers.ModelSerializer):
	class Meta:
		model = Team
		fields = ('name', 'elo', 'description')

class PlayerTeamSerializer(serializers.ModelSerializer):
	teams = TeamSerializer(many=True)

	class Meta:
		model = DotaPlayer
		fields = ('teams')