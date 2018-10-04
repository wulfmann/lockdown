
class TriggerType:
	PROC_NAME, PROC_CWD, PROC_PID = range(3)


class Action:
	
	''' One action per trigger
	trigger type must be valid TriggerType enum
	trigger must be a string; process name, directory|subdirectory
	action must be a single function, this function can obviously call as many helpers
		as needed
	'''
	
	def __init__(self, trigger_type, trigger, action):
		self._trigger_type = trigger_type
		self._trigger = trigger
		self._action = action
		assert isinstance(self._trigger_type, int)
		assert isinstance(self._trigger, str)
		assert callable(self._action)

	@property
	def trigger_type(self):
		return self._trigger_type
		
	@property
	def trigger(self):
		return self._trigger.lower()
		
	@property
	def action(self):
		return self._action
