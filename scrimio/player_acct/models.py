from django.db import models
from django.contrib.auth.models import User
import dota_mm

class Player(models.Model):
	user = models.OneToOneField(User, primary_key=True, related_name="player", on_delete=models.CASCADE) # Proxies the django User
	username = models.SlugField(unique=True, max_length=15, default=("NotFound%s" % id))
	is_online = models.BooleanField(default=False) # Is user currently online?
	steam_id = models.CharField(max_length=29, default='null', blank=True) 	# Steam ID used to connect to Steam Games
	bnet_id = models.CharField(max_length=19, default='null', blank=True) # BNet User ID to connect to BNet Games
	friends = models.ManyToManyField("self", blank=True)

	def save(self, **kwargs):
		super(Player, self).save(**kwargs)						# Save instance of Player
		dota_player = dota_mm.models.DotaPlayer(user_acct=self)	# Auto-make DotaPlayer (Non-circular import method)
		dota_player.save()										# Commit to DB

	def __unicode__(self):
		return self.username