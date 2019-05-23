# 盤面をまるごと持っているクラス。
# プレイヤーから見た視点のworldクラスも
#一緒に持っておいた方がいいかもしれない
import playerAttributes as PA
import cardInformation as CI
import copy
class visibleWorld(object):
	"""docstring for visibleWorld"""
	def __init__(self,_world=None):
		super(visibleWorld,self).__init__()
		self.LEFT=0
		self.hands=[PA.hand(),PA.hand()]
		self.graves=[PA.grave(),PA.grave()]
		self.decks=[PA.deck([]),PA.deck([])]
		self.boards=[PA.board(0),PA.board(0)]
		self.players=[PA.playerStatus([],0),PA.playerStatus([],0)]
		self.turnPlayer=self.LEFT
		if not ( _world is None):
			self.fetchInformationFromWorld(_world)
			pass
	def fetchInformationFromWorld(self,_world):
		self.turnPlayer=self.LEFT
		self.hands[self.turnPlayer]=copy.deepcopy(_world.getTurnPlayerHand())
		#ダミーカードで埋める
		self.hands[self.getOpponentPlayerIndex()]=PA.hand()
		self.hands[self.getOpponentPlayerIndex()].fillByDummyCards(_world.getOpponentPlayerHand().getNumOfElements())
		self.graves[self.turnPlayer]=copy.deepcopy(_world.getTurnPlayerGrave())
		self.graves[self.getOpponentPlayerIndex()]=copy.deepcopy(_world.getOpponentPlayerGrave())
		#これもダミーカードで埋める。
		self.decks[self.turnPlayer]=PA.deck([])
		self.decks[self.turnPlayer].fillByDummyCards(_world.getTurnPlayerDeck().getNumOfElements())
		self.decks[self.getOpponentPlayerIndex()]=PA.deck([])
		self.decks[self.getOpponentPlayerIndex()].fillByDummyCards(_world.getOpponentPlayerDeck().getNumOfElements())
		self.boards[self.turnPlayer]=copy.deepcopy(_world.getTurnPlayerBoard())
		self.boards[self.getOpponentPlayerIndex()]=copy.deepcopy(_world.getOpponentPlayerBoard())
		self.players[self.turnPlayer]=copy.deepcopy(_world.getTurnPlayer())
		self.players[self.getOpponentPlayerIndex()]=copy.deepcopy(_world.getOpponentPlayer())
		pass
	def getTurnPlayer(self):
		return self.players[self.turnPlayer]
		pass
	def getTurnPlayerHand(self):
		return self.hands[self.turnPlayer]
		pass
	def getTurnPlayerBoard(self):
		return self.boards[self.turnPlayer]
		pass
	def getTurnPlayerGrave(self):
		return self.graves[self.turnPlayer]
		pass
	def getOpponentPlayer(self):
		return self.players[self.getOpponentPlayerIndex()]
	def getOpponentPlayerHand(self):
		return self.hands[self.getOpponentPlayerIndex()]
		pass
	def getOpponentPlayerBoard(self):
		return self.boards[self.getOpponentPlayerIndex()]
		pass
	def getOpponentPlayerGrave(self):
		return self.graves[self.getOpponentPlayerIndex()]
		pass
	def getTurnPlayerIndex(self):
		return self.turnPlayer
		pass
	def getOpponentPlayerIndex(self):
		return 1-self.turnPlayer
	def getTurnPlayerDeck(self):
		return self.decks[self.turnPlayer]
		pass
	def getOpponentPlayerDeck(self):
		return self.decks[self.getOpponentPlayerIndex()]
		pass
		pass
class world(visibleWorld):
	"""docstring for world"""
	def __init__(self,_leftCardList,_rightCardList,_manaLimit=5,_boardLimit=3):
		super().__init__()
		self.RIGHT=1
		self.decks=[PA.deck(_leftCardList),PA.deck(_rightCardList)]
		self.boards=[PA.board(_boardLimit),PA.board(_boardLimit)]
		self.players=[PA.playerStatus(_leftCardList,_manaLimit),PA.playerStatus(_rightCardList,_manaLimit)]
		self.turnPlayer=self.LEFT
		pass
	def dumpWorld(self):
		print("current turn is {turn}, the left player is...".format(turn=self.turnPlayer))
		pass
	def dealACardX(self):
		self.objectPlayerDeck=self.decks[self.getTurnPlayerIndex()]
		if self.objectPlayerDeck.getNumOfElements()>0:
			self.addTurnPlayerHand(self.objectPlayerDeck.getElements().pop())
			pass
		else:
			self.players[self.getTurnPlayerIndex()].setLife(0)
		pass
	def dealCardsX(self,num):
		for x in range(num):
			self.dealACardX()
			pass
		pass
	def dealACardToOpponentX(self):
		self.objectPlayerDeck=self.decks[self.getOpponentPlayerIndex()]
		if self.objectPlayerDeck.getNumOfElements()>0:
			self.addOpponentPlayerHand(self.objectPlayerDeck.getElements().pop())
			pass
		else:
			self.players[self.getOpponentPlayerIndex()].setLife(0)
		pass
	def dealCardsToOpponentX(self,num):
		for x in range(num):
			self.dealACardToOpponentX()
			pass
		pass
	def discardX(self,index):
		self.discardedCard=self.hands[self.turnPlayer].getElements().pop(index)
		self.addTurnPlayerGrave(self.discardedCard)
		pass
	def discardOpponentX(self,index):
		self.hands[self.getOpponentPlayerIndex()].getElements().pop(index)
		pass
	def addTurnPlayerHand(self,_card):
		self.hands[self.turnPlayer].addElements(CI.card(_card))
		pass
	def addOpponentPlayerHand(self,_card):
		self.hands[self.getOpponentPlayerIndex()].addElements(CI.card(_card))
		pass
	def addTurnPlayerBoard(self,_card):
		self.boards[self.turnPlayer].addElements(CI.creature(_card))
		pass
	def addOpponentPlayerBoard(self,_card):
		self.boards[self.getOpponentPlayerIndex()].addElements(CI.creature(_card))
		pass
	def addTurnPlayerGrave(self,_card):
		self.graves[self.turnPlayer].addElements(CI.card(_card))
		pass
	def addOpponentPlayerGrave(self,_card):
		self.graves[self.getOpponentPlayerIndex()].addElements(CI.card(_card))
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
	def getPlayerBoard(self,index):
		if type(index) is int :
			if index==1 or index==0:
				return self.boards[index]
				pass
			else :
				pass
			pass
		return self.boards[self.turnPlayer]
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