from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Player

# This does NOT include friends list or User object
class PlayerDataSerializer(serializers.ModelSerializer):
	#user = serializers.PrimaryKeyRelatedField(many=False, queryset=User.objects.all())

	class Meta:
		model = Player
		fields = ('username', 'steam_id', 'bnet_id', 'is_online',)

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