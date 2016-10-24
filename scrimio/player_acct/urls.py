from django.conf.urls import url
from . import views


urlpatterns = [
	url(r'^dashboard/$', views.player_dashboard, name='user-dashboard'),
	url(r'^new/$', views.player_new, name="player-new"),
	url(r'api/user/$', views.UserList.as_view(), name="api-player-list"),
]