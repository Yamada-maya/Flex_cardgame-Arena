import gameMaster as gm
class gmForAgent(gm.gameMaster):
	"""docstring for gmForAgent"""
	def __init__(self,_cardLists=[[],[]],_world=None,_state=None):
		super(gmForAgent, self).__init__(_cardLists)
		self.world=_world
		self.state=_state
		self.tree=self.makeGameTree(self.world,self.state)
	def getTree(self):
		return self.tree
		pass