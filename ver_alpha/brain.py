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
class ruleBaseBrain(baseBrain):
	"""docstring for ruleBaseBrain"""
	def __init__(self):
		super(ruleBaseBrain, self).__init__()
						
	def chooseBestMove(self,_world,_moveList):
		self.index=0
		self.values=list(map(lambda m:self.getActionValue(_world,m["tree"]),_moveList))
		print(_moveList)
		print(self.values)
		self.index=self.values.index(max(self.values))
		return _moveList[self.index]
		pass
	def getActionValue(self,_world,_move):
		return self.simulateUntilEndOfMyTurn(_world,_move)
		pass
	def simulateUntilEndOfMyTurn(self,_world,_gameTreePromise):
		# return a value of board.
		# 自分の最後の盤面であればその時の評価値を返す。
		# それ以外であれば最大値を返す的な…
		self.nextTreeList=_gameTreePromise()
		self.nextWorld=self.nextTreeList.getWorld()
		if self.nextWorld.getTurnPlayerIndex()!=_world.getTurnPlayerIndex():
			return self.calculateWorldValue(_world)
		return max(list(map(lambda m:self.simulateUntilEndOfMyTurn(self.nextWorld,m.getGameTreePromise()),self.nextTreeList.getMoves())))
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