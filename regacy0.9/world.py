# 盤面をまるごと持っているクラス。
# プレイヤーから見た視点のworldクラスも
#一緒に持っておいた方がいいかもしれない
import playerAttributes as PA
import cardInformation as CI
class visibleWorld(object):
	"""docstring for visibleWorld"""
	def __init__(self,_world=None):
		super(visibleWorld,self).__init__()
		"""
		self.LEFT=0
		self.hands=[PA.hand(),PA.hand()]
		self.graves=[PA.grave(),PA.grave()]
		self.decks=[PA.deck(_leftCardList),PA.deck(_rightCardList)]
		self.boards=[PA.board(_boardLimit),PA.board(_boardLimit)]
		self.players=[PA.playerStatus(_leftCardList,_manaLimit),PA.playerStatus(_rightCardList,_manaLimit)]
		self.turnPlayer=self.LEFT"""
		pass
		
class world(visibleWorld):
	"""docstring for world"""
	def __init__(self,_leftCardList,_rightCardList,_manaLimit=5,_boardLimit=3):
		super().__init__()
		self.LEFT=0
		self.RIGHT=1
		self.hands=[PA.hand(),PA.hand()]
		self.graves=[PA.grave(),PA.grave()]
		self.decks=[PA.deck(_leftCardList),PA.deck(_rightCardList)]
		self.boards=[PA.board(_boardLimit),PA.board(_boardLimit)]
		self.players=[PA.playerStatus(_leftCardList,_manaLimit),PA.playerStatus(_rightCardList,_manaLimit)]
		self.turnPlayer=self.LEFT
		pass
	def dumpWorld(self):
		print("current turn is {turn}, the left player is...".format(turn=self.turnPlayer))
		pass
	def dealACardX(self):
		self.turnPlayerDeck=self.decks[self.turnPlayer]
		if self.turnPlayerDeck.getNumOfElements()>0:
			self.addTurnPlayerHand(self.turnPlayerDeck.getElements().pop())
			pass
		else:
			self.players[self.getTurnPlayerIndex()].setLife(0)
		pass
	def dealCardsX(self,num):
		for x in range(num):
			self.dealACardX()
			pass
		pass
	def addTurnPlayerHand(self,_cardName):
		self.hands[self.turnPlayer].addElements(CI.card(_cardName))
		pass
	def addTurnPlayerBoard(self,_card):
		self.boards[self.turnPlayer].addElements(CI.creature(_card))
		pass
	def addOpponentPlayerBoard(self,_card):
		self.boards[self.getOpponentPlayerIndex()].addElements(CI.creature(_card))
		pass
	def addTurnPlayerGrave(self,_creature):
		self.graves[self.turnPlayer].addElements(CI.card(_creature))
		pass
	def addOpponentPlayerGrave(self,_creature):
		self.graves[self.getOpponentPlayerIndex()].addElements(CI.card(_creature))
		pass
	def getTurnPlayer(self):
		return self.players[self.turnPlayer]
		pass
	def getOpponentPlayer(self):
		return self.players[self.getOpponentPlayerIndex()]
		pass
	def getTurnPlayerHand(self):
		return self.hands[self.turnPlayer]
		pass
	def getOpponentPlayerHand(self):
		return self.hands[self.getOpponentPlayerIndex()]
		pass
	def getTurnPlayerBoard(self):
		return self.boards[self.turnPlayer]
		pass
	def getOpponentPlayerBoard(self):
		return self.boards[self.getOpponentPlayerIndex()]
		pass
	def getTurnPlayerGrave(self):
		return self.graves[self.turnPlayer]
		pass
	def getOpponentPlayerGrave(self):
		return self.graves[self.getOpponentPlayerIndex()]
		pass
	def getTurnPlayerDeck(self):
		return self.decks[self.turnPlayer]
		pass
	def shiftNextTurn(self):
		self.turnPlayer=1-self.turnPlayer
		pass
	def getHands(self):
		return self.hands
		pass
	def getGraves(self):
		return self.graves
		pass
	def getBoards(self):
		return self.boards
		pass
	def getPlayers(self):
		return self.players
		pass
	def getDecks(self):
		return self.decks
		pass
	def getPlayerHand(self,index):
		if type(index) is int:
			if index==1 and index==0:
				return self.boards[index]
				pass
			pass
		return self.boards[self.turnPlayer]
		pass
	def getPlayerBoard(self,index):
		if type(index) is int :
			if index==1 or index==0:
				return self.boards[index]
				pass
			else :
				pass
			pass
		return self.boards[self.turnPlayer]
	def getTurnPlayerIndex(self):
		return self.turnPlayer
		pass
	def getOpponentPlayerIndex(self):
		return 1-self.turnPlayer
		pass
	def expandTurnPlayerMana(self):
		self.players[self.turnPlayer].expandMana()
		pass
	def expandOpponetnPlayerMana(self):
		self.players[self.getOpponentPlayerIndex()].expandMana()
		pass
	def recoverTurnPlayerMana(self):
		self.players[self.turnPlayer].recoverMana()
		pass
	def recoverOpponetnPlayerMana(self):
		self.players[self.getOpponentPlayerIndex()].recoverMana()
		pass
	def untapTurnPlayerCreatures(self):
		for item in self.boards[self.turnPlayer].getElements():
			item.standUp()
			pass
		pass
	def sendDeadCreaturesFromBoards(self):
		self.deadUnits=list(filter(lambda item:not item.isAlive(),self.boards[self.getTurnPlayerIndex()].getElements()))
		self.newBoard=list(filter(lambda item:item.isAlive(),self.boards[self.getTurnPlayerIndex()].getElements()))
		self.boards[self.getTurnPlayerIndex()].deleteAllElements()
		for item in self.deadUnits:
			self.graves[self.getTurnPlayerIndex()].addElements(item)
			pass
		for item in self.newBoard:
			self.boards[self.getTurnPlayerIndex()].addElements(item)
			pass
		self.deadUnits=list(filter(lambda item:not item.isAlive(),self.boards[self.getOpponentPlayerIndex()].getElements()))
		self.newBoard=list(filter(lambda item:item.isAlive(),self.boards[self.getOpponentPlayerIndex()].getElements()))
		self.boards[self.getOpponentPlayerIndex()].deleteAllElements()
		for item in self.deadUnits:
			self.graves[self.getOpponentPlayerIndex()].addElements(item)
			pass
		for item in self.newBoard:
			self.boards[self.getOpponentPlayerIndex()].addElements(item)
			pass
		pass