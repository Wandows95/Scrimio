from django.test import TestCase
from rest_framework.test import APIClient
from .app_settings import GAME_NAME
from django.urls import reverse

# Create your tests here.
class TeamAPITestCase(TestCase):
	def setUp(self):
		self.client = APIClient()
	def test_can_create_team(self):
		response = self.client.post(reverse('%s:api-team-list' % GAME_NAME), {'name':'Test', 'description':'This team sucks'}, format='json')
		try:
			assert response.status_code == 200
		except AssertionError as e:
			if response.status_code == 302:
				e.args = (('[302] User was not authenticated before creating post'),)
			else:
				e.args = (('Invalid Team Post Response: %s' % response.status_code), )
			raise