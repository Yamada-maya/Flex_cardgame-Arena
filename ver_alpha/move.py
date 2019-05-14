class move(object):
	"""docstring for move"""
	def __init__(self,_description=None,_gameTreePromise=None,_simulationTree=None):
		super(move, self).__init__()
		self.description = None
		self.gameTreePromise=None
		self.simulationTree=None
		self.setDescription(_description)
		self.setGameTreePromise(_gameTreePromise)
		self.setSimulateTree(_simulationTree)
	def setDescription(self,_description=None):
		if _description is None:
			pass
		else:
			self.description=_description
		pass
	def getDescription(self):
		return self.description
		pass
	def setGameTreePromise(self,_gameTreePromise=None):
		if _gameTreePromise is None:
			pass
		else:
			self.gameTreePromise=_gameTreePromise
		pass
	def getGameTreePromise(self):
		return self.gameTreePromise
		pass
	def setSimulateTree(self,_simulationTree):
		if _simulationTree is None:
			pass
		else:
			self.simulationTree=_simulationTree
		pass
	def getSimulateTree(self):
		return self.simulationTree
		pass