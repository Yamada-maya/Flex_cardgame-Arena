import copy
import random
import gmForAgent as gm
class baseBrain(object):
	"""docstring for baseBrain"""
	def __init__(self):
		super(baseBrain, self).__init__()
		self.mainActions=["play a card","activate a skill","attack by creature"]
	def chooseBestMove(self,_world,_moveList,_state):
		#implement this point!!
		#_moveList=[move,move,move,...,move]
		#move is composed of,"index", "description", and "tree".
		return _moveList[0]
		pass
	def getGameResult(self,_won):
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
	def developOwnDeck(self,_cardList,_ruleList):
		self.retList=[]
		self.hit=_ruleList["deck_min"]
		self.l=[]
		for item in _cardList:
			for index in range(_ruleList["max_per_card"]):
				self.l.append(copy.deepcopy(item))
				pass
			pass
		self.denominator=len(self.l)
		for item in self.l:
			if random.random()<self.hit/self.denominator:
				self.retList.append(copy.deepcopy(item))
				self.hit-=1
				pass
			self.denominator-=1
			pass
		return self.retList
		pass
	def chooseBestMove(self,_world,_moveList,_state):
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
class ruleBaseBrain(baseBrain):
	"""docstring for ruleBaseBrain"""
	def __init__(self):
		super(ruleBaseBrain, self).__init__()
	def chooseBestMove(self,_world,_moveList,_state):
		if len(_moveList)==1:
			return _moveList[0]
			pass
		self.index=0
		self.values=list(map(lambda m:self.getActionValue(_world,m["tree"],_description=m["description"]),_moveList))
		self.index=self.values.index(max(self.values))
		return _moveList[self.index]
		pass
	def getActionValue(self,_world,_move,_description=None):
		return self.simulateUntilEndOfMyTurn(_world,_move,_description=_description)
		pass
	def simulateUntilEndOfMyTurn(self,_world,_gameTreePromise,_description=None,_recursive=0):
		# return a value of board.
		# 自分の最後の盤面であればその時の評価値を返す。
		# それ以外であれば最大値を返す的な…
		self.nextTree=_gameTreePromise()
		if len(self.nextTree.getMoves())==0:
			return 0
			pass
		self.nextWorld=self.nextTree.getWorld()
		if self.nextWorld.getTurnPlayerIndex()!=_world.getTurnPlayerIndex():
			return self.calculateWorldValue(_world)
		return max(list(map(lambda m:self.simulateUntilEndOfMyTurn(self.nextWorld,m.getGameTreePromise(),_description=m.getDescription(),_recursive=_recursive+1),self.nextTree.getMoves())))
		pass
	def calculateWorldValue(self,_world):
		self.opponentLife=_world.getOpponentPlayer().getLife()
		self.handValue=_world.getTurnPlayerHand().getNumOfElements()
		self.turnPlayerBoard=_world.getTurnPlayerBoard().getElements()
		self.boardValue=self.calculateBoardValue(self.turnPlayerBoard)
		self.opponentPlayerBoard=_world.getOpponentPlayerBoard().getElements()
		self.opponentBoardValue=self.calculateBoardValue(self.opponentPlayerBoard)
		self.currentMana=_world.getTurnPlayer().getCurrentMana()
		return self.handValue+self.boardValue-self.opponentBoardValue-self.opponentLife/2-self.currentMana
		pass
	def calculateBoardValue(self,_boardElements):
		return sum(list(map(lambda e:e.getCurrentPower(),_boardElements)))
		pass