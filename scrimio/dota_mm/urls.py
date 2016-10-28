from django.conf.urls import url
from . import views

urlpatterns = [
	url(r'^$', views.Index, name="index"),
	# Team Generic View
	url(r'^teams/create/$', views.TeamCreate, name="team-create"),
	# Team Specific View
	url(r'^teams/(?P<pk>[0-9]+)/$', views.TeamView, name="team-view"),
	url(r'^teams/(?P<pk>[0-9]+)/edit', views.TeamEditView, name="team-edit"),
	# User Specific View
	url(r'^user/teams/$', views.PlayerTeamView, name="player-team-list"),
	# User Specific API
	url(r'^api/user/(?P<pk>[0-9]+)/teams/$', views.PlayerTeamList.as_view(), name="api-team-player-list"),
	# Team Generic API
	url(r'^api/teams/$', views.TeamList.as_view(), name="api-team-list"),
	# Team Specific API
	url(r'^api/team/(?P<pk>[0-9]+)/$', views.TeamDetail.as_view(), name="api-team-detail"),
	url(r'^api/team/(?P<pk>[0-9]+)/update/$', views.TeamEdit.as_view(), name="api-team-update"),
	url(r'^api/team/(?P<pk>[0-9]+)/destroy/$', views.TeamDelete.as_view(), name="api-team-destroy"),
]