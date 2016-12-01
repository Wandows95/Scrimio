from django.conf.urls import url
from . import views


urlpatterns = [
	url(r'^dashboard/$', views.player_dashboard, name='user-dashboard'),
	url(r'^friends/$', views.player_friends_list, name='user-friends'),
	url(r'^new/$', views.player_new, name="player-new"),
	url(r'^api/user/$', views.UserList.as_view(), name="api-player-list"),
	url(r'^api/user/(?P<pk>[0-9]+)/$', views.UserDetail.as_view(), name="api-player-detail"),
]