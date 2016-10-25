from django.shortcuts import render, redirect
from rest_framework import generics
from .serializers import TeamSerializer, PlayerTeamSerializer
from django.views.decorators.csrf import requires_csrf_token

from .models import Team, DotaPlayer

#------------# Generic Pages #-------------#

def Index(request):
	return render(request, 'dota_mm/index.html')

#--------------# Team Pages #--------------#

@requires_csrf_token # Ensure CSRF token is given despite lack of {% csrf_token %} in template
def TeamCreate(request):
	if request.user.is_authenticated():
		return render(request, 'dota_mm/create_team.html')
	else:
		return redirect('index')

def TeamView(request, pk):
	if request.user.is_authenticated():
		return render(request, 'dota_mm/view_team.html', {'team_id' : pk})

def PlayerTeamView(request):
	if request.user.is_authenticated():
		return render(request, 'dota_mm/view_player_teams.html', {'player_id':request.user.pk})

#---------------# Team API #---------------#

# Get list of all teams
class TeamList(generics.ListCreateAPIView):
	queryset = Team.objects.all()
	serializer_class = TeamSerializer

# Get detail of specific team
class TeamDetail(generics.RetrieveAPIView):
    queryset = Team.objects.all()
    serializer_class = TeamSerializer

# Get teams of a specific DotaPlayer
class PlayerTeamList(generics.RetrieveAPIView):
	queryset = DotaPlayer.objects.all()
	serializer_class = PlayerTeamSerializer