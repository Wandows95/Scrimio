from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Player

# Serializer for Player GET Actions
#	- Does not include friends or owning Django User
#	- Stops recursive friends list lookup
class PlayerDataSerializer(serializers.ModelSerializer):

	class Meta:
		model = Player
		fields = ('username', 'steam_id', 'bnet_id', 'is_online',)

# Serializer for Player PATCH/POST Actions
#	- Does not include owning Django User
#	- Friends list only produces Player data of friends
class PlayerSerializer(serializers.ModelSerializer):
	friends = PlayerDataSerializer(many=True, default={})

	def create(self, validated_data):
		request = self.context.get("request")

		if request and hasattr(request, "user"):
			validated_data["user"] = request.user
			player = Player.objects.create(**validated_data)
			return player
		else:
			return None

	class Meta:
		model = Player
		fields = ('username', 'steam_id', 'bnet_id', 'friends', 'is_online',)