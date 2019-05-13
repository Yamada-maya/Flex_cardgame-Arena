class gameTree(object):
	"""docstring for gameTree"""
	def __init__(self, _world=None,_moves=None):
		super(gameTree, self).__init__()
		self.world = None
		self.moves=None
		self.setWorld(_world)
		self.setMoves(_moves)
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
