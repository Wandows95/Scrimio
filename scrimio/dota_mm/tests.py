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
		self.user_1 = User.objects.create(username='test_cpt')
		Player.objects.create(user=self.user_1, username='test_cpt')
		self.user_2 = User.objects.create(username='test_child')
		Player.objects.create(user=self.user_2, username='test_child')
		self.client = APIClient()
		print("[SETUP] Test Users: %s & %s" % (self.user_1, self.user_2))

	def test_team_valid_CRUD_actions(self):
		self.client.force_authenticate(user=self.user_1) # Authenticate user as captain for valid CRUD

		post_response = self.client.post(reverse('%s:api-team-list' % GAME_NAME), {'name':'Test', 'description':'This team sucks'}, format='json')
		patch_response = self.client.patch(reverse('%s:api-team-update' % GAME_NAME, kwargs={'pk':'1'}), {'name':'EditedTeam', 'description':'This team does NOT suck'}, format='json')
		get_response = self.client.get(reverse('%s:api-team-detail' % GAME_NAME, kwargs={'pk':'1'}))
		delete_response = self.client.delete(reverse('%s:api-team-destroy' % GAME_NAME, kwargs={'pk':'1'}))
		
		self.client.force_authenticate(user=None) # Log user out for subsequent tests
		try:
			assert post_response.status_code == 201
			print("[POST] Team Created Successfully: [%s : %s]" % (post_response.data['name'], post_response.data['description'],))
			assert patch_response.status_code == 200
			print("[PATCH] Team Partial Updated Successful")
			assert get_response.status_code == 200 and get_response.data['name'] == 'EditedTeam'
			print("[GET] Team Data Received: [%s : %s]" % (get_response.data['name'], get_response.data['description'],))
			assert Team.objects.all().count() == 0 # Ensure no Teams exist post-delete
			print("[DELETE] Team Delete Successful!")

		except AssertionError as e:
			if post_response.status_code == 302:
				e.args = (('[302] User was not authenticated before creating Team'),)
			if get_response.status_code == 404:
				e.args = (('[404] Attempting GET request on non-existant Team'),)
			raise

	def test_team_invalid_CRUD_actions(self):
		self.client.force_authenticate(user=self.user_1) # Authenticate user as captain for team
		post_response = self.client.post(reverse('%s:api-team-list' % GAME_NAME), {'name':'Test', 'description':'This team sucks'}, format='json')
		self.client.force_authenticate(user=None) # De-authenticate user as captain for team
		self.client.force_authenticate(user=self.user_2) # Authenticate intruder for invalid CRUD
		patch_response = self.client.patch(reverse('%s:api-team-update' % GAME_NAME, kwargs={'pk':'1'}), {'name':'EditedTeam', 'description':'This team does NOT suck'}, format='json')
		
		try:
			assert patch_response.status_code == 403
			print("[PATCH] Intruder was successfully denied!")
		except AssertionError as e:
			e.args = ("[PATCH] Intruder was allowed in")