import copy
import random
class baseBrain(object):
	"""docstring for baseBrain"""
	def __init__(self):
		super(baseBrain, self).__init__()
		self.mainActions=["play a card","activate a skill","attack by creature"]
	def chooseBestMove(self,_world,_moveList):
		#implement this point!!
		#_moveList=[move,move,move,...,move]
		#move is composed of,"index", "description", and "tree".
		return _moveList[0]
		pass
	def developOwnDeck(self,_cardList,_ruleList):
		self.retList=[]
		for item in _cardList:
			self.retList.append(copy.deepcopy(item))
			self.retList.append(copy.deepcopy(item))
			pass
		return self.retList
		pass
class randomBrain(baseBrain):
	"""docstring for randomBrain"""
	def __init__(self):
		super(randomBrain, self).__init__()
	def chooseBestMove(self,_world,_moveList):
		self.index=0
		if _moveList[0]["description"] in self.mainActions:
			self.weight=self.getNumOfRegalActions(_moveList)
			self.pivot=int(random.random()*sum(self.weight))
			self.temp=0
			for i,item in enumerate(self.weight):
				self.temp+=item
				if self.pivot<self.temp:
					return _moveList[i]
					pass
				pass
			pass
		else:
			self.index=int(random.random()*len(_moveList))
		return _moveList[self.index]
		pass
	def getNumOfRegalActions(self,_moveList):
		self.retVals=[]
		for item in _moveList:
			self.retVals.append(len(item["tree"]().getMoves()))
			pass
		return self.retVals
		pass
		
		