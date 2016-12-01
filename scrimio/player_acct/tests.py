from django.test import TestCase
from rest_framework.test import APIClient
from django.urls import reverse
from django.contrib.auth.models import User
from player_acct.models import Player

# Player CREATE Action Tests
class PlayerCreateTestCase(TestCase):
	def setUp(self):
		self.user_1 = User.objects.create(username='test_cpt')
		self.user_2 = User.objects.create(username='test_child')
		self.client = APIClient()

	# Test that API created Players are automatically linked to a User account	
	def test_user_is_linked_automatically(self):
		self.client.force_authenticate(user=self.user_1) 			# Authenticate user as captain for valid CRUD
		post_response = self.client.post(reverse('user:api-player-list'), {'username':'TestBoi'}, format='json')
		new_player = Player.objects.get(pk=1)
		self.client.force_authenticate(user=None)					# De-Auth user from client

		try:
			self.assertEqual(post_response.status_code, 201) 		# Post Success
			self.assertNotEqual(new_player, None) 					# User was created
			self.assertEqual(new_player.user.pk, self.user_1.pk)	# Authenticated user was linked to player

		except AssertionError as e:
			print(post_response)
			raise

	# Test the integrity of the Player->User link via the public API
	def test_player_user_link_cannot_be_injected(self):
		self.client.force_authenticate(user=self.user_1) # Authenticate user as captain for valid CRUD

		# Attempt to inject self.user_2 as Player's user while user_1 is the current auth'd user
		post_response = self.client.post(reverse('user:api-player-list'), {'username':'TestBoi', 'user':self.user_2.pk}, format='json')
		new_player = Player.objects.get(pk=1)

		try:
			self.assertNotEqual(new_player.user.pk, self.user_2.pk)
		except AssertionError as e:
			raise