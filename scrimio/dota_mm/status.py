'''
Matchmaker account status definitions.

Used to determine state of user
'''
OFFLINE=0
ONLINE=1
READY=2
IN_QUEUE=3
IN_MATCH=4

GAMEPLAYER_STATUS_CHOICES=(
	(OFFLINE,0),
	(ONLINE,1),
	(READY,2),
	(IN_QUEUE,3),
	(IN_MATCH,4),
)

MUTEX_STATUS={
	READY,
	IN_QUEUE,
	IN_MATCH,
}