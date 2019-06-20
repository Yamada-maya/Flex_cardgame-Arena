import copy
import random
class playerStatus(object):
	"""docstring for playerStatus"""
	def __init__(self,_cardList,_rule={"initial_life":10,"mana_max":5}):
		super(playerStatus, self).__init__()
		self.LIFE=_rule["initial_life"]
		self.currentMana=0
		self.maxMana=0
		self.cardList=_cardList
		self.manaLimit=_rule["mana_max"]
	def consumeMana(self,num):
		self.currentMana-=num
		pass
	def getLife(self):
		return self.LIFE
		pass
	def gainLife(self,num):
		self.LIFE+=num
		pass
	def setLife(self,num):
		self.LIFE=num
		pass
	def dealDamage(self,_damage):
		self.LIFE-=_damage
		pass
	def getMaxMana(self):
		return self.maxMana
		pass
	def getCurrentMana(self):
		return self.currentMana
	def isAlive(self):
		return self.LIFE>0
		pass
	pass
	def expandMana(self):
		self.maxMana+=1
		pass
	def recoverMana(self):
		self.currentMana=self.maxMana
		pass
class factor(object):
	"""docstring for factor"""
	def __init__(self):
		super(factor, self).__init__()
		self.elements = []
	def getElements(self):
		return self.elements
	def addElements(self,_additionalElement):
		self.additionalElement=copy.deepcopy(_additionalElement)
		self.elements.append(self.additionalElement)
		pass
	def getNumOfElements(self):
		return len(self.elements)
		pass
	def deleteAllElements(self):
		self.elements=[]
		pass
	def fillByDummyCards(self,_n):
		self.dummyCard={
		"cardName": "dummy",
		"baseCost": 0,
		"baseToughness": 1,
		"basePower": 1,
		"cardType": {
			"main": "",
			"sub": [	]
			},
		"skills": {}
		}
		for i in range(_n):
			self.addElements(self.dummyCard)
			pass
		pass
	pass

class hand(factor):
	"""docstring for hand"""
	def __init__(self):
		super(hand, self).__init__()
		self.costBonus=0

class board(factor):
	"""docstring for board
	creature と land とかに分けておいた方がいいか…？"""
	def __init__(self,_boardLimit):
		super(board, self).__init__()
		self.boardLimit=_boardLimit
		self.attackBonus=[0 for i in range(_boardLimit)]
		self.toughnessBonus=[0 for i in range(_boardLimit)]
		self.skillBonus=[0 for i in range(_boardLimit)]
	def isBoardFull(self):
		return self.getNumOfElements() >=self.boardLimit
		pass

class grave(factor):
	"""docstring for grave"""
	def __init__(self):
		super(grave, self).__init__()

class deck(factor):
	"""docstring for deck"""
	def __init__(self, _cardList):
		super(deck, self).__init__()
		self.cardList = _cardList
		self.elements=copy.deepcopy(self.cardList)
		self.shuffle()
	def shuffle(self):
		for i,item in enumerate(self.elements):
			self.index=int(random.random()*(len(self.elements)-i))+i
			self.temp=item
			self.elements[i]=self.elements[self.index]
			self.elements[self.index]=self.temp
			pass
		return 
		pass
