from django.contrib.auth.models import User
from .models import Player
from django.shortcuts import render
from rest_framework import generics
from .serializers import PlayerSerializer
from django.views.decorators.csrf import requires_csrf_token

from player_acct.models import Player

#--------------# User Pages #--------------#
def explode(request):
	print('LOL')
'''
	player = Player.objects.get(username='Calypse')
	player.friends.add(20,21,22,23,24,25,26,27,28,29)
	player.save()

	print(player.friends)
	return render(request, 'player_acct/dashboard.html', {'user': request.user,'player_id': request.user.pk})

	users = []
	players = []

	for i in range(100):
		user = User.objects.create_user(first_name='User%dFirstName' % i, 
                last_name='User%dLastName' % i,
                username='user%d' % i,
                email='user%d@mydomain.com' % i,
                password='hashedPasswordStringPastedHereFromStep1!',
                is_active=True)
		user.save()

		player = Player.objects.create(user=user, username='User%d' % i)
		player.save()
'''

def player_dashboard(request):
	username = None
	if request.user.is_authenticated():
		try: 
			player = Player.objects.get(user=request.user) # Try to find this player
			user = request.user
			return render(request, 'player_acct/dashboard.html', {'user': user,'player_id': request.user.pk})
		except Player.DoesNotExist:
			return render(request, 'player_acct/user_new.html', {'user': request.user})
	#else: # Redirect to login page

def player_friends_list(request):
	if request.user.is_authenticated():
		try: 
			player = Player.objects.get(user=request.user) # Try to find this player
			user = request.user
			return render(request, 'player_acct/friends_list.html', {'user': user})
		except Player.DoesNotExist:
			return render(request, 'player_acct/user_new.html', {'user': request.user})

@requires_csrf_token # Ensure CSRF token is given despite lack of {% csrf_token %} in template
def player_new(request):
	if request.user.is_authenticated():
		try:
			player = Player.objects.get(user=request.user) # Try to find this player
		except Player.DoesNotExist: # Redirect to new player form player not found
			player = None
			return render(request, 'player_acct/user_new.html', {'user': request.user})

		return render(request, 'player_acct/dashboard.html', {'user':request.user})

	return render(request, 'scrimio/index.html')

#---------------# User API #---------------#
class UserList(generics.ListCreateAPIView):
	queryset = Player.objects.all()
	serializer_class = PlayerSerializer

class UserDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Player.objects.all()
    serializer_class = PlayerSerializer








