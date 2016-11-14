from django.test import TestCase
from rest_framework.test import APIClient

# Create your tests here.
class TeamAPITestCase(TestCase):
	def setUp(self):
		self.client = APIClient()
	def can_create_team(self):
