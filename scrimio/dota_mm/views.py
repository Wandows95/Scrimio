from .app_settings import APP_NAME, GAME_NAME
from django.shortcuts import render, redirect
from rest_framework import generics
from .serializers import TeamSerializer, PlayerTeamSerializer
from django.views.decorators.csrf import requires_csrf_token

from .models import Team, GamePlayer

#------------# Generic Pages #-------------#

def Index(request):
	return render(request, APP_NAME.format('/index.html'))

#--------------# Team Pages #--------------#

@requires_csrf_token # Ensure CSRF token is given despite lack of {% csrf_token %} in template
def TeamCreate(request):
	if request.user.is_authenticated():
		return render(request, build_url('/create_team.html'), {'user': request.user, 'player_id': request.user.pk})
	else:
		return redirect('index')

def TeamView(request, pk):
	if request.user.is_authenticated():
		return render(request, build_url('/view_team.html'), {'team_id' : pk})

@requires_csrf_token # Ensure CSRF token is given despite lack of {% csrf_token %} in template
def TeamEditView(request, pk):
	try:
		team = Team.objects.get(pk=pk)
	except Team.DoesNotExist:
		# Team doesn't even exist
		return render(request, 'scrimio/index.html')

	if request.user.is_authenticated() and team.captain.id == request.user.pk:
		return render(request, build_url('/edit_team.html'), {'user':request.user, 'teamPK':pk})

def PlayerTeamView(request):
	if request.user.is_authenticated():
		return render(request, build_url('/view_player_teams.html'), {'player_id':request.user.pk})


#---------------# Team API #---------------#

# Get list of all teams
class TeamList(generics.CreateAPIView):
	queryset = Team.objects.all()
	serializer_class = TeamSerializer

class TeamDelete(generics.DestroyAPIView):
	queryset = Team.objects.all()
	serializer_class = TeamSerializer

class TeamEdit(generics.UpdateAPIView):
	queryset = Team.objects.all()
	serializer_class = TeamSerializer

# Get detail of specific team
class TeamDetail(generics.RetrieveAPIView):
    queryset = Team.objects.all()
    serializer_class = TeamSerializer

# Get teams of a specific GamePlayer
class PlayerTeamList(generics.RetrieveAPIView):
	queryset = GamePlayer.objects.all()
	serializer_class = PlayerTeamSerializer

#---------# Utility Functions #------------#

# Builds url based on endpoint and app_name using modulo
def build_url(endpoint):
	info = (APP_NAME, endpoint)
	return("%s%s" % info)