from django.test import TestCase
from rest_framework.test import APIClient
from .app_settings import GAME_NAME
from django.urls import reverse
from django.contrib.auth.models import User
from player_acct.models import Player
from .models import Team

# Create your tests here.
class TeamAPITestCase(TestCase):
	def setUp(self):
		self.user = User(username='test_bud')
		self.user.save()
		player = Player(user=self.user, username='test_bud')
		player.save()
		self.client = APIClient()
		self.client.force_authenticate(user=self.user)
		print("Test User: %s" % self.user.username)

	def test_can_create_team(self):
		response = self.client.post(reverse('%s:api-team-list' % GAME_NAME), {'name':'Test', 'description':'This team sucks'}, format='json')
		try:
			assert response.status_code == 201
			print(Team.objects.all())
		except AssertionError as e:
			if response.status_code == 302:
				e.args = (('[302] User was not authenticated before creating post'),)
			else:
				e.args = (('Invalid Team Post Response: %s' % response.status_code), )
			raise

	def test_can_get_team(self):
		response = self.client.get(reverse('%s:api-team-detail' % GAME_NAME, kwargs={'pk':0}))
		try:
			assert response.status_code == 200
		except AssertionError as e:
			if response.status_code == 302:
				e.args = (('[302] User was not authenticated before creating post'),)
			else:
				e.args = (('Invalid Team Post Response: %s' % response.status_code), Team.objects.all())
			raise