from django.conf.urls import url
from . import views

urlpatterns = [
	url(r'^teams/create/$', views.TeamCreate, name="team-create"),
	url(r'^teams/(?P<pk>[0-9]+)/$', views.TeamView, name="team-view"),
	url(r'^user/teams/$', views.PlayerTeamView, name="player-team-list"),
	url(r'^api/user/(?P<pk>[0-9]+)/teams/$', views.PlayerTeamList.as_view(), name="api-team-player-list"),
	url(r'^api/teams/$', views.TeamList.as_view(), name="api-team-list"),
	url(r'^api/team/(?P<pk>[0-9]+)/$', views.TeamDetail.as_view(), name="api-team-detail"),
]