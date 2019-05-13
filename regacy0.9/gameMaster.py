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
class gameMaster(object):
	"""docstring for gameMaster"""
	def __init__(self,_cardLists):
		super(gameMaster, self).__init__()
		self.leftCardList=_cardLists[0]
		self.rightCardList=_cardLists[1]
		self.nextPhaseDict={
		"init":"draw",
		"draw":"main",
		"main":"end",
		"end":"init"
		}
		self.mainAction=[
		"play a card","activate skill","attack by creature"
		]
		self.manaLimit=5
		self.boardLimit=3
	def cloneWorld(self,_world):
		self.newWorld=copy.deepcopy(_world)
		return self.newWorld
		pass
	def createInitialWorld(self,_leftCardList,_rightCardList,_manaLimit,_boardLimit):
		self.retWorld=w.world(_leftCardList,_rightCardList,_manaLimit,_boardLimit)
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
		self.retTree=gt.gameTree(_world,self.listPossibleMoves(_world,_state))
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
		def shiftNextPhase():
			self.wn=self.cloneWorld(_world)
			return self.makeGameTree(self.wn,_state={"phase":self.nextPhaseDict[_state["phase"]]})
			pass
		def doNothing():
			self.wn=self.cloneWorld(_world)
			return self.makeGameTree(self.wn,_state={"phase":_state["phase"]})
			pass
		self.retMoves=move.move()
		if _state["phase"]=="gameSet":
			def inner():
				self.wn=self.createInitialWorld(self.leftCardList,self.rightCardList,self.manaLimit,self.boardLimit)
				return self.makeGameTree(self.wn,_state={"phase":"init"})
				pass
			self.retMoves.setDescription("reset game")
			self.retMoves.setGameTreePromise(self.delay(inner))
			return [self.retMoves]
			pass
		if self.isGameEnded(_world):
			def inner():
				self.wn=self.createInitialWorld(self.leftCardList,self.rightCardList,self.manaLimit,self.boardLimit)
				return self.makeGameTree(self.wn,_state={"phase":"gameSet"})
				pass
			self.winner="LEFT"
			if self.getWinnerIndex(_world)==1:
				self.winner="RIGHT"
				pass
			self.retMoves.setDescription("game set. winner is {_winner}".format(_winner=self.winner))
			self.retMoves.setGameTreePromise(self.delay(inner))
			return [self.retMoves]
		if _state["phase"]=="init":
			self.retMoves.setDescription("untap, upkeep")
			def inner():
				#untap and upkeep.
				self.wn=self.cloneWorld()
				self.wn.untapTurnPlayerCreatures()
				if self.wn.getTurnPlayer().getMaxMana()<self.manaLimit:
					self.wn.expandTurnPlayerMana()
					pass
				self.wn.recoverTurnPlayerMana()
				return self.makeGameTree(self.wn,_state={"phase":self.nextPhaseDict[_state["phase"]]})
				pass
			self.retMoves.setGameTreePromise(self.delay(inner))

			return [self.retMoves]
			pass
		if _state["phase"]=="draw":
			self.retMoves.setDescription("draw a card.")
			def inner():
				self.wn=self.cloneWorld(_w)
				self.wn.dealCardsX(1)
				return self.makeGameTree(self.wn,_state={"phase":self.nextPhaseDict[_state["phase"]]})
			self.retMoves.setGameTreePromise(self.delay(inner))
			return [self.retMoves]
			pass
		if _state["phase"]=="main" :
			if not ("opt" in _state.keys()):
				def getBasicMoves(_opt):
					def inner():
						self.wn=self.cloneWorld(_world)
						self.optState=_opt.split(" ")[0]
						return self.makeGameTree(self.wn,_state={"phase":_state["phase"],"opt":self.optState})
						pass
					self.m=move.move()
					self.m.setDescription(_opt)
					self.m.setGameTreePromise(self.delay(inner))
					return self.m
					pass
				self.retMoves=list(map(getBasicMoves,self.mainAction))
				self.additionalMove=move.move()
				self.additionalMove.setDescription("do nothing.")
				self.additionalMove.setGameTreePromise(self.delay(shiftNextPhase))
				self.retMoves.append(self.additionalMove)
				return self.retMoves
				pass
			if _state["opt"]=="play":
				def playCard(playingCardTuple):
					def inner():
						self.wn=self.cloneWorld(_world)
						return self.makeGameTree(self.wn,_state={"phase":_state["phase"],"opt":_state["opt"],"playingCardTuple":playingCardTuple})
						pass
					self.m=move.move()
					self.m.setDescription("play "+str(playingCardTuple[1]))
					self.m.setGameTreePromise(self.delay(inner))
					return self.m
					pass
				self.turnPlayerHand=_world.getTurnPlayerHand().getElements()
				self.retMoves=[]
				if _world.getTurnPlayerBoard().getNumOfElements()<self.boardLimit:
					self.currentMana=_world.getTurnPlayer().getCurrentMana()
					self.playableHand=list(filter(lambda item:CI.card(item).getCurrentCost()<=self.currentMana,self.turnPlayerHand))
					self.retMoves=list(map(playCard,list(enumerate(self.playableHand))))
					pass
				self.additionalMove=move.move()
				self.additionalMove.setDescription("don't play any card.")
				self.additionalMove.setGameTreePromise(self.delay(doNothing))
				self.retMoves.append(self.additionalMove)
				return self.retMoves
				pass

			if _state["opt"]=="activate":
				def activateSkill(_actionCardTuple):
					def inner():
						self.wn=self.cloneWorld(_world)
						return self.makeGameTree(self.wn,_state={"phase":_state["phase"],"opt":_state["opt"] ,"playingCardTuple":_actionCardTuple})
						pass
					self.m=move.move()
					self.m.setDescription("activate {card}'s skill".format(card=str(_actionCardTuple[1])))
					self.m.setGameTreePromise(self.delay(inner))
					return self.m
					pass
				self.turnPlayerBoard=_world.getTurnPlayerBoard().getElements()
				self.actionableUnit=list(filter(lambda item:item.hasSkillsByType("activate"),self.turnPlayerBoard))
				self.retMoves=list(map(activateSkill,list(enumerate(self.actionableUnit))))
				self.additionalMove=move.move()
				self.additionalMove.setDescription("no skill activate")
				self.additionalMove.setGameTreePromise(self.delay(doNothing))
				self.retMoves.append(self.additionalMove)
				return self.retMoves
				pass
			if _state["opt"]=="attack":
				def attackByCreature(_attackCardTuple):
					def inner():
						self.wn=self.cloneWorld(_world)
						return self.makeGameTree(self.wn,_state={"phase":_state["phase"],"opt":_state["opt"],"playingCardTuple":_attackCardTuple})
						pass
					self.m=move.move()
					self.m.setDescription("attack by {card}".format(card=str(_attackCardTuple[1])))
					self.m.setGameTreePromise(self.delay(inner))
					return self.m
				def noAction():
					self.wn=self.cloneWorld(_world)
					return self.makeGameTree(self.wn,_state={"phase":_state["phase"]})
					pass
				self.retMoves=[]
				self.turnPlayerBoard=_world.getTurnPlayerBoard().getElements()
				self.attackableUnit=list(filter(lambda item:item.isStand(),self.turnPlayerBoard))
				self.retMoves=list(map(attackByCreature,list(enumerate(self.attackableUnit))))
				self.additionalMove=move.move()
				self.additionalMove.setDescription("no unit action")
				self.additionalMove.setGameTreePromise(self.delay(noAction))
				self.retMoves.append(self.additionalMove)
				return self.retMoves
				pass
		if _state["phase"]=="end":
			self.retMoves.setDescription("end your turn.")
			def inner():
				self.wn=self.cloneWorld(_world)
				self.wn.shiftNextTurn()
				return self.makeGameTree(self.wn,_state={"phase":self.nextPhaseDict[_state["phase"]]})
				pass
			self.retMoves.setGameTreePromise(self.delay(inner))
			return [self.retMoves]
			pass
		pass
	def listPossibleMovesByCards(self,_world,_state):
		self.retMoves=move.move()
		def doNothing():
			self.wn=self.cloneWorld(_world)
			return self.makeGameTree(self.wn,_state={"phase":_state["phase"]})
			pass
		if _state["phase"]=="init":
			self.retMoves.setDescription("untap, upkeep")
			def inner():
				#untap and upkeep. 
				self.wn=self.cloneWorld(_world)
				return self.makeGameTree(self.wn,{"phase":self.nextPhaseDict[_state["phase"]]})
				pass
			self.retMoves.setGameTreePromise(self.delay(inner))
			return [self.retMoves]
		if _state["phase"]=="draw":
			self.retMoves.setDescription("untap, upkeep")
			def inner():
				#untap and upkeep. 
				self.wn=self.cloneWorld(_world)
				return self.makeGameTree(self.wn,{"phase":self.nextPhaseDict[_state["phase"]]})
				pass
			self.retMoves.setGameTreePromise(self.delay(inner))
			return [self.retMoves]
		if _state["phase"]=="main":
			if _state["opt"]=="play":
				#カードを使用。
				#_state["playingCardTuple"]に使っているカードが収納されている。
				if _state["playingCardTuple"][1].getMainCardType()=="creature":
					if "step" in _state.keys():
						if _state["playingCardTuple"][1].hasSkillsByType("permanent"):
							#permanent-->常在型能力
							pass
						if _state["playingCardTuple"][1].hasSkillsByType("cip"):
							#cip-->召喚時
							def solveCip():
								#cipを定義していく。
								#複数cipを持っていて、選択の余地がある場合に困っている
								self.wn=self.cloneWorld(_world)
								self.cip=_state["playingCardTuple"][1].getSkillNamesByType("cip")
								self.objectCreature=self.wn.getTurnPlayerBoard().getElements()[-1]
								if "haste" in self.cip:
									self.objectCreature.standUp()
									pass
								if "cantrip" in self.cip:
									self.wn.dealCardsX(1)
									pass
								pass
								return self.makeGameTree(self.wn,_state={"phase":_state["phase"]})
							self.retMoves.setDescription("solve cip.")
							self.retMoves.setGameTreePromise(self.delay(solveCip))
							return [self.retMoves]
							pass
						else:
							pass
							self.retMoves.setDescription("nothing happened.")
							self.retMoves.setGameTreePromise(self.delay(doNothing))
							return [self.retMoves]
					else:
						def inner():
							#playingCardを盤面に加える 
							self.wn=self.cloneWorld(_world)
							self.playedCard=self.wn.getTurnPlayerHand().getElements().pop(_state["playingCardTuple"][0])
							self.wn.addTurnPlayerBoard(self.makeCreature(self.playedCard))
							self.wn.getTurnPlayer().consumeMana(self.playedCard.getCurrentCost())
							return self.makeGameTree(self.wn,_state={"phase":_state["phase"],"opt":_state["opt"],"playingCardTuple":_state["playingCardTuple"],"step":"solveEffect"})
							pass
						self.retMoves.setDescription("solve playing {card}".format(card=_state["playingCardTuple"][1]))
						self.retMoves.setGameTreePromise(self.delay(inner))
						return [self.retMoves]
						pass
				if _state["playingCardTuple"].getMainCardType()=="land":
					pass
				if _state["playingCardTuple"].getMainCardType()=="sorcery":
					pass
				pass
			if _state["opt"]=="activate":
				if "step" in _state.keys():
					if _state["activateSkill"]["name"]=="looter":
						if _state["step"]=="discard":
							def chooseDiscard(_handTuple):
								def inner():
									self.wn=self.cloneWorld(_world)
									self.disCardObject=self.wn.getTurnPlayerHand().getElements().pop(_handTuple[0])
									return self.makeGameTree(self.wn,_state={"phase":_state["phase"]})
									pass
								pass
								self.m=move.move()
								self.m.setDescription("discard {card}.".format(card=str(_handTuple[1])))
								self.m.setGameTreePromise(self.delay(inner))
								return self.m
							self.turnPlayerHand=_world.getTurnPlayerHand().getElements()
							self.retMoves=list(map(chooseDiscard,enumerate(self.turnPlayerHand)))
							return self.retMoves
							pass
						if _state["step"]=="paid":
							def inner():
								self.wn=self.cloneWorld(_world)
								self.wn.dealCardsX(1)
								self.argState=_state
								self.argState["step"]="discard"
								return self.makeGameTree(self.wn,_state=self.argState)
								pass
							self.retMoves.setDescription("draw a card.")
							self.retMoves.setGameTreePromise(self.delay(inner))
							return [self.retMoves]
				if "activateSkill" in _state.keys():
					def canPayCosts(_skill):
						if not(_skill["cost"]["tap"]) or not (_state["playingCardTuple"][1].isStand()):
							return False
						if _skill["cost"]["mana"]>_world.getTurnPlayer().getCurrentMana():
							return False
						if _skill["cost"]["discard"]>_world.getTurnPlayerHand().getNumOfElements():
							return False
						if _skill["cost"]["sacrifice"]>_world.getTurnPlayerBoard().getNumOfElements():
							return False
							pass
						return True
						pass
					if canPayCosts(_state["activateSkill"]):
						def activateSkill():
							self.wn=self.cloneWorld(_world)
							if _state["activateSkill"]["cost"]["tap"]:
								#起動しているクリーチャー情報が欲しいからタプルにする必要あるかも
								self.wn.getTurnPlayerBoard().getElements()[_state["playingCardTuple"][0]].tapThisCreature()
								pass
							return self.makeGameTree(self.wn,_state={"phase":_state["phase"],"opt":_state["opt"],"playingCardTuple":_state["playingCardTuple"],"activateSkill":_state["activateSkill"],"step":"paid"})	
							pass
						self.retMoves=[]
						self.activateMove=move.move()
						self.activateMove.setDescription("pay {skillCost}".format(skillCost=_state["playingCardTuple"][1].skillCostToString(_state["activateSkill"]["cost"])))
						self.activateMove.setGameTreePromise(self.delay(activateSkill))
						self.retMoves.append(self.activateMove)
						self.additionalMove.setDescription("refuse paying cost.")
						self.additionalMove.setGameTreePromise(self.delay(doNothing))
						self.retMoves.append(self.additionalMove)
						return self.retMoves
					else:
						self.retMoves.setDescription("can't pay cost.")
						self.retMoves.setGameTreePromise(self.delay(doNothing))
						return [self.retMoves]
					pass

				else:
					self.skills=_state["playingCardTuple"][1].getSkillsByType("activate")
					def activateSkill(_skill):
						def inner():
							self.wn=self.cloneWorld(_world)
							print(_skill)
							return self.makeGameTree(self.wn,{"phase":_state["phase"],"opt":_state["opt"],"playingCardTuple":_state["playingCardTuple"],"activateSkill":_skill})
							pass
						self.m=move.move()
						self.m.setDescription("activate {_skill}".format(_skill=_skill["name"]))
						self.m.setGameTreePromise(self.delay(inner))
						return self.m
						pass
					self.retMoves=list(map(activateSkill,self.skills))
					self.additionalMove=move.move()
					self.additionalMove.setDescription("activate no skill.")
					self.additionalMove.setGameTreePromise(self.delay(doNothing))
					return self.retMoves
					pass
			if _state["opt"]=="attack":
				def decideAttackObject(_defenseCreatureTuple):
					def inner():
						self.wn=self.cloneWorld(_world)
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
					self.m.setGameTreePromise(self.delay(inner))
					return self.m
				def bodyAttack():
					self.wn=self.cloneWorld(_world)
					self.tb=self.wn.getPlayerBoard(self.wn.getTurnPlayerIndex()).getElements()
					self.attackCard=self.tb[_state["playingCardTuple"][0]]
					self.op=self.wn.getOpponentPlayer()
					self.op.dealDamage(self.attackCard.getCurrentPower())
					self.attackCard.tapThisCreature()
					return self.makeGameTree(self.wn,{"phase":_state["phase"]})
					pass
				self.opponentBoard=_world.getOpponentPlayerBoard()
				self.retMoves=list(map(decideAttackObject,list(enumerate(self.opponentBoard.getElements()))))
				self.additionalMove=move.move()
				self.additionalMove.setDescription("attack body")
				self.additionalMove.setGameTreePromise(self.delay(bodyAttack))
				self.retMoves.append(self.additionalMove)
				return self.retMoves
				pass
		if _state["phase"]=="end":
			self.retMoves.setDescription("untap, upkeep")
			def inner():
				#untap and upkeep. 
				self.wn=self.cloneWorld(_world)
				self.wn.shiftNextTurn()
				return self.makeGameTree(self.wn,{"phase":self.nextPhaseDict[_state["phase"]]})
				pass
			self.retMoves.setGameTreePromise(self.delay(inner))
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
