class gameTree(object):
	"""docstring for gameTree"""
	def __init__(self, _world=None,_moves=None,_state=None):
		super(gameTree, self).__init__()
		self.world = None
		self.moves=None
		self.state=None
		self.setWorld(_world)
		self.setMoves(_moves)
		self.setState(_state)
	def setWorld(self,_world=None):
		if _world is None:
			pass
		else:
			self.world=_world
		pass
	def getWorld(self):
		return self.world
		pass
	def setMoves(self,_moves=None):
		if _moves is None:
			pass
		else:
			self.moves=_moves
		pass
	def getMoves(self):
		return self.moves
		pass
	def setState(self,_state=None):
		if _state is None:
			pass
		else:
			self.state=_state
		pass
	def getState(self):
		return self.state
		pass
