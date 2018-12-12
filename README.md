# Scrimio: Esports matchmaking prototype

Scrimio is a platform that arranges games based on skill rating (ELO).
Each game supported by the service gets it's own player/group queue,
where the matchmaker pulls and builds matches based on each team's ELO rating.

The matchmaker's goal is to minimize the difference between each team's skill rating.

### Dependencies:
  - django>1.10
  - channels
  - djangorestframework
  - django-libsass
  - django_compressor
  - python-social-auth
  - asgi_redis
  - trueskill
