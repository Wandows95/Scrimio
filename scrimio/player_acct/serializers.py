from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Player

class PlayerSerializer(serializers.ModelSerializer):
	user = serializers.PrimaryKeyRelatedField(many=False, queryset=User.objects.all())
	friends = serializers.PrimaryKeyRelatedField(queryset=Player.objects.all(), many=True)

	class Meta:
		model = Player
		fields = ('user', 'username', 'steam_id', 'bnet_id', 'friends')
