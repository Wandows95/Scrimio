'''
Matchmaker account status

Used to determine state of user
'''
OFFLINE=0
ONLINE=1
READY=2
IN_QUEUE=3
IN_MATCH=4

# Model 'choices' formatted list
GAMEPLAYER_STATUS_CHOICES=(
	(OFFLINE,0),
	(ONLINE,1),
	(READY,2),
	(IN_QUEUE,3),
	(IN_MATCH,4),
)

# Statuses that cannot be transitioned to from ANY state
MUTEX_STATUS={
	READY,
	IN_QUEUE,
	IN_MATCH,
}

def status_is_transition_allowed(prv_state, new_state):
	'''
	Status state transition rules
	'''
	if new_state not in MUTEX_STATUS and prv_state not in MUTEX_STATUS:
		return True

	# If naturally next step
	if new_state == prv_state+1:
		return True

	# If tranferring to previous step (and not locked in to match)
	if prv_state < IN_MATCH and new_state == prv_state - 1:
		return True

	# If returning from match
	if prv_state > IN_QUEUE and new_state < READY:
		return True

	return False
