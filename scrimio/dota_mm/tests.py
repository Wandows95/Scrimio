from django.test import TestCase
from rest_framework.test import APIClient
from .app_settings import GAME_NAME, TEAM_SIZE
from django.urls import reverse
from django.contrib.auth.models import User
from player_acct.models import Player
from .models import Team, GamePlayer
from channels import Channel
from channels.tests import ChannelTestCase, HttpClient
from .status import MUTEX_STATUS, OFFLINE, ONLINE, READY, IN_QUEUE

from .matchmaking import mm_can_team_queue

import json


class TeamAPIBasicActionTestCase(TestCase):
	'''
	API Basic use case tests
	'''
	def setUp(self):
		self.user_1 = User.objects.create(username='test_cpt')
		Player.objects.create(user=self.user_1, username='test_cpt')
		self.user_2 = User.objects.create(username='test_child')
		Player.objects.create(user=self.user_2, username='test_child')
		self.client = APIClient()
	
	def test_team_valid_CRUD_actions(self):
		'''
		#Test that all CRUD Actions can be performed on Team Model via API
		'''
		# Authenticate user as captain for valid CRUD
		self.client.force_authenticate(user=self.user_1)
		# Create new test Team
		post_response = self.client.post(reverse('%s:api-team-list' % GAME_NAME), {'name':'Test', 'description':'This team sucks'}, format='json')
		# Update the name and description of Team
		patch_response = self.client.patch(reverse('%s:api-team-update' % GAME_NAME, kwargs={'pk':'1'}), {'name':'EditedTeam', 'description':'This team does NOT suck', 'players':[2,],}, format='json')
		# Retrieve the newly modified Team
		get_response = self.client.get(reverse('%s:api-team-detail' % GAME_NAME, kwargs={'pk':'1'}))
		# Delete the test Team
		delete_response = self.client.delete(reverse('%s:api-team-destroy' % GAME_NAME, kwargs={'pk':'1'}))
		# Log user out for subsequent tests
		self.client.force_authenticate(user=None) 
		
		try:
			self.assertEqual(post_response.status_code, 201)
			self.assertEqual(patch_response.status_code, 200)
			self.assertEqual(get_response.status_code, 200)
			self.assertEqual(get_response.data['name'], 'EditedTeam')
			self.assertEqual(Team.objects.all().count(), 0)
			# Verify user was posted
			self.assertEqual(len(get_response.data['players']), 1)
			# Verify user data is correct
			self.assertEqual(get_response.data['players'][0]['user_acct']['username'], 'test_child')
		
		except:
			if post_response.status_code == 302:
				print('[302] User was not authenticated before creating Team')
			if get_response.status_code == 404:
				print('[404] Attempting GET request on non-existant Team')
			raise

	def test_team_unauthorized_CRUD_actions(self):
		'''
		Test that constraints on Patch and Delete are valid via API
		'''
		# Authenticate user as captain for team
		self.client.force_authenticate(user=self.user_1)
		# Create new test Team
		post_response = self.client.post(reverse('%s:api-team-list' % GAME_NAME), {'name':'Test', 'description':'This team sucks'}, format='json')
		# De-authenticate user as captain for team
		self.client.force_authenticate(user=None) 		
		# Authenticate intruder for invalid CRUD	
		self.client.force_authenticate(user=self.user_2) 	
		# Intruder attempt to maliciously update Team
		patch_response = self.client.patch(reverse('%s:api-team-update' % GAME_NAME, kwargs={'pk':'1'}), {'name':'EditedTeam', 'description':'This team does NOT suck'}, format='json')
		# Intruder attempts to maliciously delete Team
		delete_response = self.client.delete(reverse('%s:api-team-destroy' % GAME_NAME, kwargs={'pk':'1'}))
		
		try:
			self.assertEqual(patch_response.status_code, 403)
			self.assertEqual(delete_response.status_code, 401)
			self.assertEqual(Team.objects.count(), 1)
		except:
			print("[PATCH] Unauthorized CRUD action occurred")

class TeamAPICreateActionTestCase(TestCase):
	'''
	Team Create action specific tests
	'''
	def setUp(self):
		self.user_1 = User.objects.create(username='test_cpt')
		Player.objects.create(user=self.user_1, username='test_cpt')
		self.user_2 = User.objects.create(username='test_child')
		Player.objects.create(user=self.user_2, username='test_child')
		self.client = APIClient()

	def test_team_create_cannot_inject_captain(self):
		'''
		Test that a user cannot specify who is captain of team during CREATE/POST
		'''
		# Authenticate user as captain for team
		self.client.force_authenticate(user=self.user_1)
		intruder_game_player = self.user_2.player.dota_player.get()
		# Create new test Team
		post_response = self.client.post(reverse('%s:api-team-list' % GAME_NAME), {'name':'Test', 'description':'This team sucks', 'captain':intruder_game_player.pk}, format='json')
		test_team = Team.objects.get(pk=1)
		# De-authenticate user as captain for team
		self.client.force_authenticate(user=None) 			
		
		try:
			self.assertNotEqual(test_team.captain.pk, self.user_2.pk)
		except:
			print("[PATCH] Team create allowed Captain injection",)

class TeamAPIUpdateActionTestCase(TestCase):
	'''
	Team Update action specific tests
	'''
	def setUp(self):
		self.user_1 = User.objects.create(username='test_cpt')
		Player.objects.create(user=self.user_1, username='test_cpt')
		self.user_2 = User.objects.create(username='test_child_1')
		Player.objects.create(user=self.user_2, username='test_child_1')
		self.user_3 = User.objects.create(username='test_child_2')
		Player.objects.create(user=self.user_3, username='test_child_2')
		self.client = APIClient()

	def test_team_can_update_players_field(self):
		'''
		Verify Team players field is modifiable
		'''
		# Authenticate user as captain for team
		self.client.force_authenticate(user=self.user_1) 	
		post_response = self.client.post(reverse('%s:api-team-list' % GAME_NAME), {'name':'Test', 'description':'This team sucks'}, format='json')
		patch_response = self.client.patch(reverse('%s:api-team-update' % GAME_NAME, kwargs={'pk':'1'}), {'name':'EditedTeam', 'description':'This team does NOT suck', 'players':[2,3],}, format='json')
		get_response = self.client.get(reverse('%s:api-team-detail' % GAME_NAME, kwargs={'pk':'1'}))
		# Extract team player list
		team_players = get_response.data['players']	

		# De-authenticate user as captain for team
		self.client.force_authenticate(user=None) 			
		try:
			# Verify 2 users have been added to Team
			self.assertEqual(len(team_players), 2) 
		except AssertionError:
			print("[PATCH] Team Update could not add players [Expected: 2, Current: %s]" % len(team_players))

	def test_team_can_update_captain_field(self):
		'''
		Verify Team captain field is modifiable 
		'''
		# Authenticate user as captain for team
		self.client.force_authenticate(user=self.user_1) 	
		post_response = self.client.post(reverse('%s:api-team-list' % GAME_NAME), {'name':'Test', 'description':'This team sucks'}, format='json')
		patch_response = self.client.patch(reverse('%s:api-team-update' % GAME_NAME, kwargs={'pk':'1'}), {'name':'EditedTeam', 'description':'This team does NOT suck', 'captain':2,}, format='json')
		get_response = self.client.get(reverse('%s:api-team-detail' % GAME_NAME, kwargs={'pk':'1'}))
		# Extract captain's username
		captain_username = get_response.data['captain']['user_acct']['username'] 
		# De-authenticate user as captain for team
		self.client.force_authenticate(user=None) 			

		try:
			# Verify captain has been changed
			self.assertEqual(captain_username, self.user_2.username)
		except AssertionError:
			print("[PATCH] Team Update could change captain",)

	def test_team_captain_cannot_be_player(self):
		'''
		Verify sets captain and players are mutually exclusive 
		'''
		# Authenticate user as captain for team
		self.client.force_authenticate(user=self.user_1) 	
		post_response = self.client.post(reverse('%s:api-team-list' % GAME_NAME), {'name':'Test', 'description':'This team sucks'}, format='json')
		patch_response = self.client.patch(reverse('%s:api-team-update' % GAME_NAME, kwargs={'pk':'1'}), {'name':'EditedTeam', 'description':'This team does NOT suck', 'captain':2, 'players':[2,],}, format='json')
		get_response = self.client.get(reverse('%s:api-team-detail' % GAME_NAME, kwargs={'pk':'1'}))
		# Extract captain's username
		captain_username = get_response.data['captain']['user_acct']['username']
		# De-authenticate user as captain for team
		self.client.force_authenticate(user=None)
	
		try:
			# Verify captain has been changed
			self.assertEqual(captain_username, self.user_1.username)
		except AssertionError:
			print("[PATCH] Team Update did not swap player and captain",)
	
	def test_team_duplicate_players_flattened(self):
		'''
		Verify player duplicates are removed automatically 
		'''
		# Authenticate user as captain for team
		self.client.force_authenticate(user=self.user_1) 	
		post_response = self.client.post(reverse('%s:api-team-list' % GAME_NAME), {'name':'Test', 'description':'This team sucks'}, format='json')
		patch_response = self.client.patch(reverse('%s:api-team-update' % GAME_NAME, kwargs={'pk':'1'}), {'name':'EditedTeam', 'description':'This team does NOT suck', 'players':[2,2],}, format='json')
		get_response = self.client.get(reverse('%s:api-team-detail' % GAME_NAME, kwargs={'pk':'1'}))
		# De-authenticate user as captain for team
		self.client.force_authenticate(user=None) 			
	
		try:
			# Verify duplicates were removed
			self.assertEqual(len(get_response.data['players']), 1) 
		except AssertionError:
			print("[PATCH] Duplicate players can be added",)

	def test_team_players_can_be_removed(self):
		'''
		Verify player duplicates are removed automatically 
		'''
		# Authenticate user as captain for team
		self.client.force_authenticate(user=self.user_1) 	
		post_response = self.client.post(reverse('%s:api-team-list' % GAME_NAME), {'name':'Test', 'description':'This team sucks'}, format='json')
		patch_1_response = self.client.patch(reverse('%s:api-team-update' % GAME_NAME, kwargs={'pk':'1'}), {'name':'EditedTeam', 'description':'This team does NOT suck', 'players':[2,3],}, format='json')
		get_1_response = self.client.get(reverse('%s:api-team-detail' % GAME_NAME, kwargs={'pk':'1'}))
		patch_2_response = self.client.patch(reverse('%s:api-team-update' % GAME_NAME, kwargs={'pk':'1'}), {'players':[2,],}, format='json')
		get_2_response = self.client.get(reverse('%s:api-team-detail' % GAME_NAME, kwargs={'pk':'1'}))
		# De-authenticate user as captain for team
		self.client.force_authenticate(user=None) 			

		try:
			# Verify 2 players existed
			self.assertEqual(len(get_1_response.data['players']), 2)
			# Verify 1 player was removed
			self.assertEqual(len(get_2_response.data['players']), 1) 
		except AssertionError:
			print("[PATCH] Duplicate players can be added",)

class GamePlayerAPIBasicActionTestCase(TestCase):
	'''
	API GamePlayer basic uses
	'''
	def setUp(self):
		# Build user & player, GamePlayer auto-built
		self.client = APIClient()
		self.test_user = User.objects.create(username='test_cpt')
		self.client.force_authenticate(user=self.test_user)
		self.test_player = Player.objects.create(user=self.test_user, username='test_player')
	def test_can_get_player_detail(self):
		self.get_response = self.client.get(reverse('%s:api-player-detail' % GAME_NAME, kwargs={'pk':'1'}))
		try:
			self.assertEqual(self.get_response.status_code, 200)
			self.assertEqual(self.get_response.data['elo'], 500)
		except AssertionError:
			print("[GET] GamePlayer could not be found",)

	def test_can_get_player_team_list(self):
		# Create new test Team
		self.post_response = self.client.post(reverse('%s:api-team-list' % GAME_NAME), {'name':'Test', 'description':'This team sucks'}, format='json')
		self.get_response = self.client.get(reverse('%s:api-team-player-list' % GAME_NAME, kwargs={'pk':'1'}))
		#try:
			#self.assertFalse(self.get_response.data['captain_of'][0]['captain']['is_ready'])
		#except:
		#	print('[GET] GamePlayer\'s ready status is not set')

class QueueSocketsBasicTestCase(ChannelTestCase):
	'''
	Basic Websocket Function tests
	'''
	def setUp(self):
		self.test_user = User.objects.create(username='test_cpt')
		self.client = HttpClient()
		# Authenticate user
		self.client.force_login(user=self.test_user)
		self.test_player = Player.objects.create(user=self.test_user, username='test_player')
		self.test_game_player = GamePlayer.objects.get(user_acct=self.test_player)
		self.test_team = Team.objects.create(name="TESTER", description='LOL', captain=self.test_game_player)

		self.endpoint_path = '/%s/sockets/status/TESTER/' % GAME_NAME

	def test_connect_and_disconnect(self):
		'''
		Test if connect/disconnect events are reflected in database
		'''
		# Craft message with predictable reply channel & send
		con_message={'text':json.dumps({'team_name':'TESTER'}), 'reply_channel':'test-queue-receive'}
		self.client.send_and_consume(channel='websocket.connect', path=self.endpoint_path, content=con_message)
		con_response = json.loads(self.get_next_message('test-queue-receive', require=True)['text'])
		con_mm_status = GamePlayer.objects.get(user_acct=self.test_player).status
		
		dis_message={'text':json.dumps({'team_name':'TESTER'}), 'reply_channel':'test-queue-receive'}
		self.client.send_and_consume(channel='websocket.disconnect', path=self.endpoint_path, content=con_message)
		dis_response = json.loads(self.get_next_message('test-queue-receive', require=True)['text'])
		dis_mm_status = GamePlayer.objects.get(user_acct=self.test_player).status
		
		try:
			# Was user logged in to queue?
			self.assertEqual(con_response['status'], ONLINE)
			self.assertEqual(con_mm_status.state, ONLINE)
			# Was the correct action returned?
			self.assertEqual(con_response['action'], 'team-queue-player-update')
		except AssertionError:
			print("[WS_QUEUE] Connect function failed! [%s] action resulted in status [%s]" % (con_response['action'], con_response['status'],))
		
		try:
			# Was user logged out of queue?
			self.assertEqual(dis_response['status'], OFFLINE)
			self.assertEqual(dis_mm_status.state, OFFLINE)
			# Was correct action returned?
			self.assertEqual(dis_response['action'], con_response['action'])
		except AssertionError:
			print("[WS_QUEUE] Disconnect function failed! [%s] action resulted in status [%s]" % (dis_response['action'], dis_response['status'],))
	
	def test_player_can_toggle_ready(self):
		'''
		Test if the server can receive and ready a new player up
		'''
		message={'text':json.dumps({'team_name':'TESTER'}), 'reply_channel':'test-queue-receive'}
		self.client.send_and_consume(channel='websocket.connect', path=self.endpoint_path, content=message)
		# Flush queued message
		self.get_next_message('test-queue-receive', require=True)

		self.client.send_and_consume(channel='websocket.receive', path=self.endpoint_path, content=message)
		rdy_response = json.loads(self.get_next_message('test-queue-receive', require=True)['text'])
		rdy_mm_status = GamePlayer.objects.get(user_acct=self.test_player).status
		
		self.client.send_and_consume(channel='websocket.receive', path=self.endpoint_path, content=message)
		un_rdy_response = json.loads(self.get_next_message('test-queue-receive', require=True)['text'])
		un_rdy_mm_status = GamePlayer.objects.get(user_acct=self.test_player).status

		try:
			self.assertEqual(rdy_response['status'], READY)
			self.assertEqual(rdy_response['action'], 'team-queue-player-update')
			self.assertEqual(rdy_mm_status.current_team, self.test_team)
		except AssertionError:
			print("[WS_QUEUE] Ready Up function failed: [%s] action resulted in status [%s] bound to team [%s]" % (rdy_response['action'], rdy_response['status'], rdy_mm_status.current_team.name))

		try:
			self.assertEqual(un_rdy_response['status'], ONLINE)
			self.assertEqual(un_rdy_response['action'], 'team-queue-player-update')
			self.assertNotEqual(un_rdy_mm_status.current_team, self.test_team)
		except AssertionError:
			print("[WS_QUEUE] Reverse Ready Up function failed: [%s] action resulted in status [%s] bound to team [%s]" % (rdy_response['action'], rdy_response['status'], rdy_mm_status.current_team.name))

	def test_unready_cannot_queue(self):
		'''
		Ensure ready matchmaking constraints are enforced on unready team
		'''
		try:
			# Test if team is unready
			self.assertFalse(mm_can_team_queue(self.test_game_player, self.test_team.players))
		except AssertionError:
			print('[MM RULES] Unready team allowed into queue')

	