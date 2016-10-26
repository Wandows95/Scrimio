from .models import Team, DotaPlayer
from player_acct.models import Player
from rest_framework import serializers


class DotaPlayerSerializer(serializers.ModelSerializer):
	user_acct = serializers.PrimaryKeyRelatedField(many=False, read_only=True)
	
	class Meta:
		model=DotaPlayer
		fields=('user_acct',)


class TeamSerializer(serializers.ModelSerializer):
	
	class Meta:
		model = Team
		fields = ('name', 'elo', 'description', 'captain',)

class PlayerTeamSerializer(serializers.ModelSerializer):
	#teams = serializers.StringRelatedField(many=True)

	class Meta:
		model = DotaPlayer
		fields = ('teams',)