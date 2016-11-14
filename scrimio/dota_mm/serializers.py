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


class TeamSerializer(serializers.Serializer):
	elo = serializers.IntegerField(read_only=True)
	players = GamePlayerSerializer(many=True, read_only=True)
	captain = GamePlayerSerializer(many=False)

	class Meta:
		model = Team
		fields = ('name', 'elo', 'description', 'captain', 'players',)

    # Use this method for the custom field
	def get_user(self):
		user = self.context['request'].user
		return user

	def create(self, validated_data):
		captain = GamePlayer.objects.get()
		#validated_data['captain'] = self.get_user()
		return Team(**validated_data)

class PlayerTeamSerializer(serializers.HyperlinkedModelSerializer):
	teams = TeamSerializer(many=True)
	captain_of = TeamSerializer(many=True)
	
	class Meta:
		model = GamePlayer
		fields = ('teams', 'captain_of',)