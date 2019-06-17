class card(object):
	"""docstring for card"""
	def __init__(self, _cardData):
		super(card, self).__init__()
		self.initCard(_cardData)
	def initCard(self,_cardData):
		if type(_cardData) is dict:
			self.statusDict=_cardData
			self.statusDict["currentCost"]=self.statusDict["baseCost"]
			pass
		elif isinstance(_cardData,card):
			self.statusDict=_cardData.statusDict
		pass
	def __eq__(self,_card):
		return self.statusDict==_card.statusDict
		pass
	def __str__(self):
		return "{name},{c}/{p}/{t}".format(name=self.getCardName(),c=self.getBaseCost(),p=self.getBasePower(),t=self.getBaseToughness())
		pass
	def getCardName(self):
		return self.statusDict["cardName"]
		pass
	def getCurrentCost(self):
		return self.statusDict["currentCost"]
		pass
	def getBaseCost(self):
		return self.statusDict["baseCost"]
		pass
	def getBasePower(self):
		return self.statusDict["basePower"]
		pass
	def getBaseToughness(self):
		return self.statusDict["baseToughness"]
		pass
	def getSkills(self):
		return self.statusDict["skills"]
		pass
	def getMainCardType(self):
		return self.statusDict["cardType"]["main"]
		pass
	def getSubCardTypes(self):
		return self.statusDict["cardType"]["sub"]
		pass
	def getSkillsByType(self,_skillType):
		if self.hasSkillsByType(_skillType):
			return self.getSkills()[_skillType]
			pass
		return []
		pass
	def getSkillNamesByType(self,_skillType):
		self.retList=[]
		if self.hasSkillsByType(_skillType):
			for item in self.getSkills()[_skillType]:
				self.retList.append(item["name"])
			pass
		return self.retList
	def getSkillCostsByType(self,_skillType):
		self.retList=[]
		if self.hasSkillsByType(_skillType):
			for item in self.getSkills()[_skillType]:
				_self.retList.append(item["cost"])
			pass
		return self.retList
	def hasSkillsByType(self,_skillType):
		return _skillType in self.getSkills().keys()
		pass
	def skillCostToString(self,_cost):
		self.retStr=""
		if self.getMainCardType()=="creature":
			if _cost["tap"]:
				self.retStr+="tap "
				pass
			if _cost["mana"]>0:
				self.retStr+="{mana}mana ".format(mana=_cost["mana"])
				pass
			if _cost["discard"]>0:
				self.retStr+="{discard}discard ".format(discard=_cost["discard"])
				pass
			if self.retStr=="":
				self.retStr+="no cost."
				pass
		self.retStr+="."
		return self.retStr
		pass

class creature(card):
	"""docstring for creature"""
	def __init__(self, _card):
		super(creature, self).__init__(_card.getCardName())
		self.initCreature(_card)
	def __eq__(self,_creature):
		if _creature is None or type(self)!=type(_creature):
			return False
		else:
			return self.statusDict==_creature.statusDict
			pass
		pass
	def __str__(self):
		return "{name},{c}/{p}/{t},{canAttack}".format(name=self.getCardName(),c=self.getCurrentCost(),p=self.getCurrentPower(),t=self.getCurrentToughness(),canAttack=self.isStand())
		pass
	def initCreature(self,_card):
		self.statusDict=_card.statusDict
		self.statusDict["currentToughness"]=self.statusDict["baseToughness"]
		self.statusDict["currentPower"]=self.statusDict["basePower"]
		self.statusDict["isStand"]=False
	def getCurrentPower(self):
		return self.statusDict["currentPower"]
		pass
	def getCurrentToughness(self):
		return self.statusDict["currentToughness"]
		pass
	def isStand(self):
		return self.statusDict["isStand"]
		pass
	def standUp(self):
		self.statusDict["isStand"]=True
		pass
	def tapThisCreature(self):
		self.statusDict["isStand"]=False
		pass
	def dealDamage(self,_damage):
		self.statusDict["currentToughness"]-=_damage
		pass
	def isAlive(self):
		return self.statusDict["currentToughness"]>0
		pass
	def addPowerBonus(self,_powerBonus):
		self.statusDict["currentPower"]+=_powerBonus
		pass
	def addToughnessBonus(self,_toughnessBonus):
		self.statusDict["currentToughness"]+=_toughnessBonus
		pass
	def addBonus(self,_powerBonus=0,_toughnessBonus=0,_bothBonus=0):
		self.addPowerBonus(_powerBonus)
		self.addToughnessBonus(_toughnessBonus)
		self.addPowerBonus(_bothBonus)
		self.addToughnessBonus(_bothBonus)
		pass