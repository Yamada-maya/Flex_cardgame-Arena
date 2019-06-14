# 困ったら、クラスにしておけ！面倒でもたぶんそれがいちばんいい。
# 長くなってもたどれるから！たぶん！
# handを変数名にしてそれを配列にする方がもっと面倒だと思います！
# と、思ったがハンドをふやしたりポップするときに面倒になったのですこし考える
import world as w
import playerAttributes as PA
import cardInformation as CI
import gameTree as gt
import move
import copy 
import json
class gameMaster(object):
	"""docstring for gameMaster"""
	def __init__(self,_cardLists=None):
		super(gameMaster, self).__init__()
		self.f=open("./data/rule.json",'r')
		self.rule=json.load(self.f)
		self.f.close()
		self.leftCardList=_cardLists[0]
		self.rightCardList=_cardLists[1]
		self.nextPhaseDict={
		"init":"draw",
		"draw":"main",
		"main":"end",
		"end":"init"
		}
		self.mainAction=[
		"play a card","activate a skill","attack by creature"
		]
		self.manaLimit=self.rule["mana_max"]
		self.boardLimit=self.rule["board_max"]
		self.initialLife=self.rule["initial_life"]
		self.initialHand=self.rule["initial_hand"]
	def cloneWorld(self,_world):
		self.newWorld=copy.deepcopy(_world)
		return self.newWorld
		pass
	def createInitialWorld(self,_leftCardList,_rightCardList,_manaLimit,_boardLimit):
		self.retWorld=w.world(_leftCardList,_rightCardList,_manaLimit,_boardLimit)
		self.retWorld.dealCardsX(self.initialHand)
		self.retWorld.dealCardsToOpponentX(self.initialHand+1)
		return self.retWorld
		pass
	def developInitialGameTree(self):
		self.wn=self.createInitialWorld(self.leftCardList,self.rightCardList,self.manaLimit,self.boardLimit)
		self.retTree=self.makeGameTree(self.wn,_state={"phase":"init"})
		return self.retTree
		pass
	def makeCard(self,_card):
		# card インスタンスにcreateCard的なのを用意する気がする
		self.retCard=CI.card(_cardName)
		return self.retCard
		pass
	def makeCreature(self,_card):
		self.retCreature=CI.creature(_card)
		return self.retCreature
		pass
	def makeGameTree(self,_world,_state):
		# ここで_stateを返すとagentに渡すときに_worldを改変させられそう
		self.retTree=gt.gameTree(_world=_world,_moves=self.listPossibleMoves(_world,_state),_state=_state)
		return self.retTree
		pass
	def listPossibleMoves(self,_world,_state):
		if "playingCardTuple" in _state.keys():
			return self.listPossibleMovesByCards(_world,_state)
			pass
		else:
			return self.listPossibleMovesByRules(_world,_state)
		pass
	def listPossibleMovesByRules(self,_world,_state):
		#フェイズも記録した方がよさげ―
		def shiftNextPhase(_w):
			self.wn=self.cloneWorld(_w)
			return self.makeGameTree(self.wn,_state={"phase":self.nextPhaseDict[_state["phase"]]})
			pass
		def doNothing(_w):
			self.wn=self.cloneWorld(_w)
			return self.makeGameTree(self.wn,_state={"phase":_state["phase"]})
			pass
		self.retMoves=move.move()
		if _state["phase"]=="gameSet":
			def inner(_w):
				self.wn=self.createInitialWorld(self.leftCardList,self.rightCardList,self.manaLimit,self.boardLimit)
				return self.makeGameTree(self.wn,_state={"phase":"init"})
				pass
			self.retMoves.setDescription("reset game")
			self.retMoves.setGameTreePromise(self.delay(inner,_world))
			self.retMoves.setSimulateTree(self.delay(inner,w.visibleWorld(_world)))
			return [self.retMoves]
			pass
		if self.isGameEnded(_world):
			def inner(_w):
				self.wn=self.createInitialWorld(self.leftCardList,self.rightCardList,self.manaLimit,self.boardLimit)
				return self.makeGameTree(self.wn,_state={"phase":"gameSet"})
				pass
			self.winner="LEFT"
			if self.getWinnerIndex(_world)==1:
				self.winner="RIGHT"
				pass
			self.retMoves.setDescription("game set. winner is {_winner}, reset game.".format(_winner=self.winner))
			_world.shiftNextTurn()
			self.retMoves.setGameTreePromise(self.delay(inner,_world))
			self.retMoves.setSimulateTree(None)
			return [self.retMoves]
		if _state["phase"]=="init":
			self.retMoves.setDescription("untap, upkeep")
			def inner(_w):
				#untap and upkeep.
				self.wn=self.cloneWorld(_w)
				self.wn.untapTurnPlayerCreatures()
				if self.wn.getTurnPlayer().getMaxMana()<self.manaLimit:
					self.wn.expandTurnPlayerMana()
					pass
				self.wn.recoverTurnPlayerMana()
				return self.makeGameTree(self.wn,_state={"phase":self.nextPhaseDict[_state["phase"]]})
				pass
			self.retMoves.setGameTreePromise(self.delay(inner,_world))
			self.retMoves.setSimulateTree(self.delay(inner,w.visibleWorld(_world)))

			return [self.retMoves]
			pass
		if _state["phase"]=="draw":
			self.retMoves.setDescription("draw a card.")
			def inner(_w):
				self.wn=self.cloneWorld(_w)
				self.wn.dealCardsX(1)
				return self.makeGameTree(self.wn,_state={"phase":self.nextPhaseDict[_state["phase"]]})
			self.retMoves.setGameTreePromise(self.delay(inner,_world))
			self.retMoves.setSimulateTree(self.delay(inner,w.visibleWorld(_world)))
			return [self.retMoves]
			pass
		if _state["phase"]=="main" :
			if not ("opt" in _state.keys()):
				def getBasicMoves(_opt):
					def inner(_w):
						self.wn=self.cloneWorld(_w)
						self.optState=_opt.split(" ")[0]
						return self.makeGameTree(self.wn,_state={"phase":_state["phase"],"opt":self.optState})
						pass
					self.m=move.move()
					self.m.setDescription(_opt)
					self.m.setGameTreePromise(self.delay(inner,_world))
					self.m.setSimulateTree(self.delay(inner,w.visibleWorld(_world)))
					return self.m
					pass
				def canPayCosts(_card,_skill):
					if _skill["cost"]["tap"] and not (_card.isStand()):
						return False
					if _skill["cost"]["mana"]>_world.getTurnPlayer().getCurrentMana():
						return False
					if _skill["cost"]["discard"]>_world.getTurnPlayerHand().getNumOfElements():
						return False
					return True
				def hasActivatableSkill(_card):
					self.skill=_card.getSkillsByType("activate")
					return len(list(filter(lambda s:canPayCosts(_card,s),self.skill)))>0
					pass
				def isPlayableAction(_opt):
					if _opt.split(" ")[0]=="play":
						def isPlayableCard(cardTuple):
							self.currentMana=_world.getTurnPlayer().getCurrentMana()
							self.turnPlayerBoard=_world.getTurnPlayerBoard()
							if cardTuple[1].getCurrentCost()>self.currentMana:
								return False
								pass
							if cardTuple[1].getMainCardType()=="creature":
								return not (self.turnPlayerBoard.isBoardFull())
								pass
							if cardTuple[1].getMainCardType()=="sorcery":
								return True
							return False
							pass
						self.turnPlayerHand=_world.getTurnPlayerHand().getElements()
						self.playableHand=list(filter(lambda item:isPlayableCard(item),enumerate(self.turnPlayerHand)))
						return len(self.playableHand)>0
						pass
					if _opt.split(" ")[0]=="activate":
						self.turnPlayerBoard=_world.getTurnPlayerBoard().getElements()
						self.skillCreatures=list(filter(lambda item:item.hasSkillsByType("activate"),self.turnPlayerBoard))
						self.activatableCreatures=list(filter(hasActivatableSkill,self.skillCreatures))
						return len(self.activatableCreatures)>0
						pass
					if _opt.split(" ")[0]=="attack" :
						self.turnPlayerBoard=_world.getTurnPlayerBoard().getElements()
						return len(list(filter(lambda item:item.isStand(),self.turnPlayerBoard)))>0
						pass
					return False
					pass
				self.playableActions=list(filter(isPlayableAction,self.mainAction))
				self.retMoves=list(map(getBasicMoves,self.playableActions))
				self.additionalMove=move.move()
				self.additionalMove.setDescription("do nothing.")
				self.additionalMove.setGameTreePromise(self.delay(shiftNextPhase,_world))
				self.additionalMove.setSimulateTree(self.delay(shiftNextPhase,w.visibleWorld(_world)))
				self.retMoves.append(self.additionalMove)
				return self.retMoves
				pass
			if _state["opt"]=="play":
				def isPlayableCard(cardTuple):
					self.currentMana=_world.getTurnPlayer().getCurrentMana()
					self.turnPlayerBoard=_world.getTurnPlayerBoard()
					if cardTuple[1].getCurrentCost()>self.currentMana:
						return False
						pass
					if cardTuple[1].getMainCardType()=="creature":
						return not (self.turnPlayerBoard.isBoardFull())
						pass
					if cardTuple[1].getMainCardType()=="sorcery":
						return True
					return False
					pass
				def playCard(playingCardTuple):
					def inner(_w):
						self.wn=self.cloneWorld(_w)
						return self.makeGameTree(self.wn,_state={"phase":_state["phase"],"opt":_state["opt"],"playingCardTuple":playingCardTuple})
						pass
					self.m=move.move()
					self.m.setDescription("play "+str(playingCardTuple[1]))
					self.m.setGameTreePromise(self.delay(inner,_world))
					self.m.setSimulateTree(self.delay(inner,w.visibleWorld(_world)))
					return self.m
					pass
				self.turnPlayerHand=_world.getTurnPlayerHand().getElements()
				self.playableHand=list(filter(lambda item:isPlayableCard(item),enumerate(self.turnPlayerHand)))
				self.retMoves=list(map(playCard,self.playableHand))
				return self.retMoves
				pass

			if _state["opt"]=="activate":
				def canPayCosts(_card,_skill):
					if _skill["cost"]["tap"] and not (_card.isStand()):
						return False
					if _skill["cost"]["mana"]>_world.getTurnPlayer().getCurrentMana():
						return False
					if _skill["cost"]["discard"]>_world.getTurnPlayerHand().getNumOfElements():
						return False
					return True
				def hasActivatableSkill(_card):
					self.skill=_card.getSkillsByType("activate")
					return len(list(filter(lambda s:canPayCosts(_card,s),self.skill)))>0
					pass
				def activateSkill(_actionCardTuple):
					def inner(_w):
						self.wn=self.cloneWorld(_w)
						return self.makeGameTree(self.wn,_state={"phase":_state["phase"],"opt":_state["opt"] ,"playingCardTuple":_actionCardTuple})
						pass

					self.m=move.move()
					self.m.setDescription("activate {card}'s skill".format(card=str(_actionCardTuple[1])))
					self.m.setGameTreePromise(self.delay(inner,_world))
					self.m.setSimulateTree(self.delay(inner,w.visibleWorld(_world)))
					return self.m
					pass
				self.turnPlayerBoard=_world.getTurnPlayerBoard().getElements()
				self.skillCreatures=list(filter(lambda item:item[1].hasSkillsByType("activate"),list(enumerate(self.turnPlayerBoard))))
				self.actionableCreatures=list(filter(lambda item:hasActivatableSkill(item[1]),self.skillCreatures))
				self.retMoves=list(map(activateSkill,self.actionableCreatures))
				return self.retMoves
				pass
			if _state["opt"]=="attack":
				def attackByCreature(_attackCardTuple):
					def inner(_w):
						self.wn=self.cloneWorld(_w)
						return self.makeGameTree(self.wn,_state={"phase":_state["phase"],"opt":_state["opt"],"playingCardTuple":_attackCardTuple})
						pass
					self.m=move.move()
					self.m.setDescription("attack by {card}".format(card=str(_attackCardTuple[1])))
					self.m.setGameTreePromise(self.delay(inner,_world))
					self.m.setSimulateTree(self.delay(inner,w.visibleWorld(_world)))
					return self.m
				def noAction(_w):
					self.wn=self.cloneWorld(_w)
					return self.makeGameTree(self.wn,_state={"phase":_state["phase"]})
					pass
				self.retMoves=[]
				self.turnPlayerBoard=_world.getTurnPlayerBoard().getElements()
				self.attackableUnitTuple=list(filter(lambda item:item[1].isStand(),enumerate(self.turnPlayerBoard)))
				self.retMoves=list(map(attackByCreature,list(self.attackableUnitTuple)))
				return self.retMoves
				pass
		if _state["phase"]=="end":
			self.retMoves.setDescription("end your turn.")
			def inner(_w):
				self.wn=self.cloneWorld(_w)
				self.wn.shiftNextTurn()
				return self.makeGameTree(self.wn,_state={"phase":self.nextPhaseDict[_state["phase"]]})
				pass
			self.retMoves.setGameTreePromise(self.delay(inner,_world))
			self.retMoves.setSimulateTree(self.delay(inner,w.visibleWorld(_world)))
			#終了時の処理は迷いマイマイ
			return [self.retMoves]
			pass
		pass
	def listPossibleMovesByCards(self,_world,_state):
		self.retMoves=move.move()
		def doNothing(_w):
			self.wn=self.cloneWorld(_w)
			return self.makeGameTree(self.wn,_state={"phase":_state["phase"]})
			pass
		if _state["phase"]=="init":
			self.retMoves.setDescription("untap, upkeep")
			def inner(_w):
				#untap and upkeep. 
				self.wn=self.cloneWorld(_w)
				return self.makeGameTree(self.wn,{"phase":self.nextPhaseDict[_state["phase"]]})
				pass
			self.retMoves.setGameTreePromise(self.delay(inner,_world))
			return [self.retMoves]
		if _state["phase"]=="draw":
			self.retMoves.setDescription("untap, upkeep")
			def inner(_w):
				#untap and upkeep. 
				self.wn=self.cloneWorld(_w)
				return self.makeGameTree(self.wn,{"phase":self.nextPhaseDict[_state["phase"]]})
				pass
			self.retMoves.setGameTreePromise(self.delay(inner,_world))
			return [self.retMoves]
		if _state["phase"]=="main":
			if _state["opt"]=="play":
				#カードを使用。
				#_state["playingCardTuple"]に使っているカードが収納されている。
				if _state["playingCardTuple"][1].getMainCardType()=="creature":
					if "step" in _state.keys():
						if _state["step"]=="burn":
							#とりあえずburn 能力は個別で発動させよう(?)
							def chooseBurnObject(opponentCardTuple):
								def inner(_w):
									self.wn=self.cloneWorld(_w)
									self.wn.getOpponentPlayerBoard().getElements()[opponentCardTuple[0]].dealDamage(2)
									self.wn.sendDeadCreaturesFromBoards()
									return self.makeGameTree(self.wn,_state={"phase":_state["phase"]})
									pass
								self.m=move.move()
								self.m.setDescription("deal 2 damage for {card}".format(card=str(opponentCardTuple[1])))
								self.m.setGameTreePromise(self.delay(inner,_world))
								self.m.setSimulateTree(self.delay(inner,w.visibleWorld(_world)))
								return self.m
								pass
							self.opponentBoard=_world.getOpponentPlayerBoard().getElements()
							if len(self.opponentBoard)>0:
								self.retMoves=list(map(chooseBurnObject ,enumerate(self.opponentBoard)))
								return self.retMoves
								pass
							else:
								self.retMoves.setDescription("there is no object.")
								self.retMoves.setGameTreePromise(self.delay(doNothing,_world))
								self.retMoves.setSimulateTree(self.delay(doNothing,w.visibleWorld(_world)))
								return [self.retMoves]
						if _state["playingCardTuple"][1].hasSkillsByType("permanent"):
							#permanent-->常在型能力
							pass
						if _state["playingCardTuple"][1].hasSkillsByType("cip"):
							#cip-->召喚時
							def solveCip(_w):
								#cipを定義していく。
								#複数cipを持っていて、選択の余地がある場合に困っている
								self.wn=self.cloneWorld(_w)
								self.cip=_state["playingCardTuple"][1].getSkillNamesByType("cip")
								self.objectCreature=self.wn.getTurnPlayerBoard().getElements()[-1]
								if "haste" in self.cip:
									self.objectCreature.standUp()
									pass
								if "cantrip" in self.cip:
									self.wn.dealCardsX(1)
									pass
								if "burn" in self.cip:
									return self.makeGameTree(self.wn,_state={"phase":_state["phase"],"opt":_state["opt"],"playingCardTuple":_state["playingCardTuple"],"step":"burn"})
									pass
								pass
								return self.makeGameTree(self.wn,_state={"phase":_state["phase"]})
							self.cipMove=move.move()
							self.cipMove.setDescription("solve cip.")
							self.cipMove.setGameTreePromise(self.delay(solveCip,_world))
							self.cipMove.setSimulateTree(self.delay(solveCip,w.visibleWorld(_world)))

							return [self.cipMove]
							pass
						else:
							pass
							self.retMoves.setDescription("nothing happened.")
							self.retMoves.setGameTreePromise(self.delay(doNothing,_world))
							self.retMoves.setSimulateTree(self.delay(doNothing,w.visibleWorld(_world)))
							return [self.retMoves]
					else:
						def inner(_w):
							#playingCardを盤面に加える 
							self.wn=self.cloneWorld(_w)
							self.playedCard=self.wn.getTurnPlayerHand().getElements().pop(_state["playingCardTuple"][0])
							self.wn.addTurnPlayerBoard(self.makeCreature(self.playedCard))
							self.wn.getTurnPlayer().consumeMana(self.playedCard.getCurrentCost())
							return self.makeGameTree(self.wn,_state={"phase":_state["phase"],"opt":_state["opt"],"playingCardTuple":_state["playingCardTuple"],"step":"solveEffect"})
							pass
						self.retMoves.setDescription("solve playing {card}".format(card=_state["playingCardTuple"][1]))
						self.retMoves.setGameTreePromise(self.delay(inner,_world))
						self.retMoves.setSimulateTree(self.delay(inner,w.visibleWorld(_world)))
						return [self.retMoves]
						pass
				elif _state["playingCardTuple"][1].getMainCardType()=="land":
					pass
				elif _state["playingCardTuple"][1].getMainCardType()=="sorcery":
					pass
				else:
					def inner(_w):
						self.wn=self.cloneWorld(_w)
						self.wn.getTurnPlayerHand().getElements().pop(_state["playingCardTuple"][0])
						print("use dummy card?")
						return self.makeGameTree(self.wn,_state={"phase":_state["phase"]})
						pass
					self.retMoves.setDescription("")
					self.retMoves.setGameTreePromise(self.delay(inner,_world))
					self.retMoves.setSimulateTree(self.delay(inner,w.visibleWorld(_world)))
					return [self.retMoves]
			if _state["opt"]=="activate":
				if "step" in _state.keys():
					if _state["activateSkill"]["name"]=="research":
						if _state["step"]=="discard":
							def chooseDiscard(_handTuple):
								def inner(_w):
									self.wn=self.cloneWorld(_w)
									self.wn.discardX(_handTuple[0])
									return self.makeGameTree(self.wn,_state={"phase":_state["phase"]})
								self.m=move.move()
								self.m.setDescription("discard {card}.".format(card=str(_handTuple[1])))
								self.m.setGameTreePromise(self.delay(inner,_world))
								self.m.setSimulateTree(self.delay(inner,w.visibleWorld(_world)))
								return self.m
							self.turnPlayerHand=_world.getTurnPlayerHand().getElements()
							self.retMoves=list(map(chooseDiscard,enumerate(self.turnPlayerHand)))
							return self.retMoves
							pass
						if _state["step"]=="paid":
							def inner(_w):
								self.wn=self.cloneWorld(_w)
								self.wn.dealCardsX(1)
								self.argState=_state
								self.argState["step"]="discard"
								return self.makeGameTree(self.wn,_state=self.argState)
								pass
							self.retMoves.setDescription("draw a card.")
							self.retMoves.setGameTreePromise(self.delay(inner,_world))
							self.retMoves.setSimulateTree(self.delay(inner,_world))
							return [self.retMoves]
					if _state["activateSkill"]["name"]=="heal":
						if _state["step"]=="paid":
							def inner(_w):
								self.wn=self.cloneWorld(_w)
								self.wn.gainTurnPlayerX(3)
								return self.makeGameTree(self.wn,_state={"phase":_state["phase"]})
								pass
							self.retMoves.setDescription("gain 3 life.")
							self.retMoves.setGameTreePromise(self.delay(inner,_world))
							self.retMoves.setSimulateTree(self.delay(inner,_world))
							return [self.retMoves]

						pass
				if "activateSkill" in _state.keys():
					def activateSkill(_w):
						self.wn=self.cloneWorld(_w)
						if _state["activateSkill"]["cost"]["tap"]:
							#起動しているクリーチャー情報が欲しいからタプルにする必要あるかも
							self.wn.getTurnPlayerBoard().getElements()[_state["playingCardTuple"][0]].tapThisCreature()
							pass
						self.wn.getTurnPlayer().consumeMana(_state["activateSkill"]["cost"]["mana"])
						return self.makeGameTree(self.wn,_state={"phase":_state["phase"],"opt":_state["opt"],"playingCardTuple":_state["playingCardTuple"],"activateSkill":_state["activateSkill"],"step":"paid"})
						pass
					self.retMoves=[]
					self.activateMove=move.move()
					self.activateMove.setDescription("pay {skillCost}".format(skillCost=_state["playingCardTuple"][1].skillCostToString(_state["activateSkill"]["cost"])))
					self.activateMove.setGameTreePromise(self.delay(activateSkill,_world))
					self.activateMove.setSimulateTree(self.delay(activateSkill,w.visibleWorld(_world)))
					self.retMoves.append(self.activateMove)
					return self.retMoves
				else:
					def canPayCosts(_card,_skill):
						if _skill["cost"]["tap"] and not (_state["playingCardTuple"][1].isStand()):
							return False
						if _skill["cost"]["mana"]>_world.getTurnPlayer().getCurrentMana():
							return False
						if _skill["cost"]["discard"]>_world.getTurnPlayerHand().getNumOfElements():
							return False
						return True
						pass
					def activateSkill(_skill):
						def inner(_w):
							self.wn=self.cloneWorld(_w)
							return self.makeGameTree(self.wn,{"phase":_state["phase"],"opt":_state["opt"],"playingCardTuple":_state["playingCardTuple"],"activateSkill":_skill})
							pass
						self.m=move.move()
						self.m.setDescription("activate {_skill}".format(_skill=_skill["name"]))
						self.m.setGameTreePromise(self.delay(inner,_world))
						self.m.setSimulateTree(self.delay(inner,w.visibleWorld(_world)))
						return self.m
						pass
					self.skills=_state["playingCardTuple"][1].getSkillsByType("activate")
					self.activatableSkills=list(filter(lambda s:canPayCosts(_state["playingCardTuple"][1],s),self.skills))#
					self.retMoves=list(map(activateSkill,self.activatableSkills))
					return self.retMoves
					pass
			if _state["opt"]=="attack":
				def decideAttackObject(_defenseCreatureTuple):
					def inner(_w):
						self.wn=self.cloneWorld(_w)
						self.tb=self.wn.getTurnPlayerBoard().getElements()
						self.ob=self.wn.getOpponentPlayerBoard().getElements()
						self.attackCard=self.tb[_state["playingCardTuple"][0]]
						self.defenseCard=self.ob[_defenseCreatureTuple[0]]
						combat(self.attackCard,self.defenseCard)
						self.wn.sendDeadCreaturesFromBoards()
						return self.makeGameTree(self.wn,{"phase":_state["phase"]})
						pass
					def combat(_attackCard,_defenseCard):
						_attackCard.dealDamage(_defenseCard.getCurrentPower())
						_defenseCard.dealDamage(_attackCard.getCurrentPower())
						_attackCard.tapThisCreature()
					self.m=move.move()
					self.m.setDescription("attack to {card}".format(card=str(_defenseCreatureTuple[1])))
					self.m.setGameTreePromise(self.delay(inner,_world))
					self.m.setSimulateTree(self.delay(inner,w.visibleWorld(_world)))
					return self.m
				def bodyAttack(_w):
					self.wn=self.cloneWorld(_w)
					self.tb=self.wn.getTurnPlayerBoard().getElements()
					self.attackCard=self.tb[_state["playingCardTuple"][0]]
					self.op=self.wn.getOpponentPlayer()
					self.op.dealDamage(self.attackCard.getCurrentPower())
					self.attackCard.tapThisCreature()
					return self.makeGameTree(self.wn,{"phase":_state["phase"]})
					pass
				self.opponentBoard=_world.getOpponentPlayerBoard()
				self.retMoves=list(map(decideAttackObject,list(enumerate(self.opponentBoard.getElements()))))
				if _world.getOpponentPlayerBoard().isBoardFull():
					pass
				else:
					self.additionalMove=move.move()
					self.additionalMove.setDescription("attack body")
					self.additionalMove.setGameTreePromise(self.delay(bodyAttack,_world))
					self.additionalMove.setSimulateTree(self.delay(bodyAttack,w.visibleWorld(_world)))
					self.retMoves.append(self.additionalMove)
				return self.retMoves
				pass
		if _state["phase"]=="end":
			self.retMoves.setDescription("untap, upkeep")
			def inner(_w):
				#untap and upkeep. 
				self.wn=self.cloneWorld(_w)
				self.wn.shiftNextTurn()
				return self.makeGameTree(self.wn,{"phase":self.nextPhaseDict[_state["phase"]]})
				pass
			self.retMoves.setGameTreePromise(self.delay(inner,_world))
			self.retMoves.setSimulateTree(self.delay(inner,w.visibleWorld(_world)))
			#終了時の処理をどうするかは迷いマイマイ
			return [self.retMoves]
			pass
		pass
	def isGameEnded(self,_world):
		self.tp=_world.getTurnPlayer()
		self.op=_world.getOpponentPlayer()
		if self.tp.isAlive() and self.op.isAlive():
			return False
		return True
		pass
	def getWinnerIndex(self,_world):
		self.tp=_world.getTurnPlayer()
		self.op=_world.getOpponentPlayer()
		if not self.tp.isAlive():
			return _world.getOpponentPlayerIndex()
		elif not self.op.isAlive():
			return _world.getTurnPlayerIndex()
		return 
		pass
	def delay(self,expressionAsFunction,arg):
		self.result=0
		self.isEvaluated=False
		def innerFunction():
			if not self.isEvaluated:
				self.isEvaluated=True
				self.result=expressionAsFunction(arg)
				pass
			return self.result
			pass
		return innerFunction
		pass
	def force(self,promise):
		return promise()
		pass
