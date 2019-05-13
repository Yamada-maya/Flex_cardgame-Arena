class move(object):
	"""docstring for move"""
	def __init__(self,_description=None,_gameTreePromise=None):
		super(move, self).__init__()
		self.description = None
		self.gameTreePromise=None
		self.gameTreeForSimulation=None
		self.setDescription(_description)
		self.setGameTreePromise(_gameTreePromise)
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