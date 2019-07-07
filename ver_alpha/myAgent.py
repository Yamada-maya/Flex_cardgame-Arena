import brain 
import gmForAgent as gm
import copy
import random
import numpy as np
import chainer
import chainer.functions as F
import chainer.links as L
import csv
import gameMaster
import world as w
from chainer import Variable, optimizers

class MyModel(chainer.Chain):
	def __init__(self):
		super(MyModel, self).__init__()
		self.droprate=0.5
		with self.init_scope():
			self.l1=L.Linear(183,512)
			self.l2=L.Linear(512,512)
			self.l3=L.Linear(512,128)
			self.l4=L.Linear(128,1)
	def __call__(self,x):
		h1=F.dropout(F.relu(self.l1(x)),ratio=self.droprate)
		h2=F.dropout(F.relu(self.l2(h1)),ratio=self.droprate)
		h3=F.dropout(F.relu(self.l3(h2)),ratio=self.droprate)
		return self.l4(h3)
		pass
class myAgent(brain.baseBrain):
	"""対戦を重ねるごとに学習をしていく感じのエージェント。"""
	def __init__(self,_cardList,_rule):
		super(myAgent, self).__init__(_cardList,_rule)
		self.model=MyModel()
		self.optimizer=optimizers.SGD()
		self.optimizer.setup(self.model)
		self.worldStack=[]
		self.currentDeck=[]
		self.deckList=[]
		self.worldToCsv=[]
		self.isLearning=True
	def developOwnDeck(self):
		self.retList=[]
		self.retList.append(copy.deepcopy(self.cardList[0]))
		self.retList.append(copy.deepcopy(self.cardList[0]))
		self.retList.append(copy.deepcopy(self.cardList[1]))
		self.retList.append(copy.deepcopy(self.cardList[1]))
		self.retList.append(copy.deepcopy(self.cardList[2]))
		self.retList.append(copy.deepcopy(self.cardList[2]))
		self.retList.append(copy.deepcopy(self.cardList[4]))
		self.retList.append(copy.deepcopy(self.cardList[4]))
		self.retList.append(copy.deepcopy(self.cardList[6]))
		self.retList.append(copy.deepcopy(self.cardList[6]))
		self.retList.append(copy.deepcopy(self.cardList[7]))
		self.retList.append(copy.deepcopy(self.cardList[7]))
		self.retList.append(copy.deepcopy(self.cardList[9]))
		self.retList.append(copy.deepcopy(self.cardList[10]))
		self.retList.append(copy.deepcopy(self.cardList[10]))
		self.retList.append(copy.deepcopy(self.cardList[13]))
		self.retList.append(copy.deepcopy(self.cardList[13]))
		self.retList.append(copy.deepcopy(self.cardList[14]))
		self.retList.append(copy.deepcopy(self.cardList[14]))
		self.retList.append(copy.deepcopy(self.cardList[15]))
		return self.retList
		pass
	def setLearningStateToFalse(self):
		self.isLearning=False
		pass
	def setLearningStateToTrue(self):
		self.isLearning=True
		pass
	def chooseBestMove(self,_world,_moveList,_state):
		if len(_moveList)==1:
			return _moveList[0]
			pass
		self.index=0
		self.tau=random.random()
		if self.tau<0.8 or (not self.isLearning):
			self.values=list(map(lambda m:self.getActionValue(_world,m["tree"],_description=m["description"]),_moveList))
			self.index=self.values.index(max(self.values))
			pass
		else:
			self.index=int(random.random()*(len(_moveList)))
		#print(self.values)
		if self.isLearning:
			self.worldStack.append(self.worldToVec(_world))
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
		if len(self.nextTree.getMoves())==0 or _recursive>10:
			return self.calculateWorldValue(_world)
			pass
		self.nextWorld=self.nextTree.getWorld()
		if self.nextWorld.getTurnPlayerIndex()!=_world.getTurnPlayerIndex():
			self.value=self.calculateWorldValue(_world)
			#print(self.value)
			return self.value
		return max(list(map(lambda m,w=self.nextWorld:self.simulateUntilEndOfMyTurn(w,m.getGameTreePromise(),_description=m.getDescription(),_recursive=_recursive+1),self.nextTree.getMoves())))
		pass
	def calculateWorldValue(self,_world):
		self.worldVec=self.worldToVec(_world)
		#print("worldVec")
		#print(self.worldVec)
		with chainer.using_config('train',False):
			self.input=Variable(np.array(self.worldVec,dtype=np.float32).reshape(1,-1))
		#print(self.model(self.input)[0][1].data)
		return self.model(self.input)[0][0].data
		pass
	def getGameResult(self,_sign):
		self.arg=0
		if _sign:
			self.arg=1
			pass
		for item in self.worldStack:
			self.l=copy.deepcopy(item)
			self.l.extend([self.arg])
			self.worldToCsv.append(self.l)
			pass
		with open("./data/situation.csv","w") as f:
			writer=csv.writer(f,lineterminator="\n")
			writer.writerows(self.worldToCsv)
		self.learn(self.arg)
		pass
	def learn(self,_sign):
		self.inputX=Variable(np.array(self.worldStack,dtype=np.float32))
		print(self.inputX.shape)
		print(self.inputX)
		self.result=[_sign for i in range(len(self.worldStack))]
		self.y=Variable(np.array(self.result,dtype=np.int32).reshape(-1,1))
		print(self.y.shape)
		print(self.y)
		for i in range(5):
			self.model.zerograds()
			self.loss=F.sigmoid_cross_entropy(self.model(self.inputX),self.y)
			print("loss={loss}".format(loss=self.loss))
			self.loss.backward()
			self.optimizer.update()
		self.worldStack=[]
		pass
	def worldToVec(self,_world):
		#self.retVec=[0 for i in range()]
		def lifeToVec(_life):
			v=[0 for i in range(6)]
			if _life<=3:
				v[0]=1
			elif _life<=6:
				v[1]=1
			elif _life<=10:
				v[2]=1
			elif _life<=18:
				v[3]=1
			elif _life<=20:
				v[4]=1
			else :
				v[5]=1
			return v
			pass
		def handToVec(_handElement):
			v=[0 for i in range(34)]
			for item in _handElement:
				if v[item.getID()]==1:
					v[item.getID()+16]=1
				else:
					v[item.getID()]=1
				pass
			return v
			pass
		def oppohandToVec(_handNum):
			v=[0 for i in range(5)]
			v[self.limitValue(_handNum,0,4)]=1
			return v
			pass
		def boardToVec(_boardElements):
			bVec=[]
			for item in _boardElements:
				bVec.extend(creatureToVec(item))
				pass
			for item in range(3-len(_boardElements)):
				bVec.extend([0 for i in range(22)])
				pass
			return bVec
			pass
		def creatureToVec(_creature):
			v=[0 for i in range(22)]
			if _creature.getCurrentPower()>2:
				v[0]=1
			else:
				v[1]=1
			if _creature.getCurrentToughness()>3:
				v[2]=1
			else:
				v[3]=1
			if _creature.isStand():
				v[4]=1
			if _creature.hasSkillsByType("activate"):
				v[5]=1
				pass
			v[_creature.getID()]=1
			return v
			pass
		self.retVec=[]
		self.retVec.extend(lifeToVec(_world.getTurnPlayer().getLife()))#6
		self.retVec.extend(lifeToVec(_world.getOpponentPlayer().getLife()))#12
		self.board=_world.getTurnPlayerBoard().getElements()
		self.retVec.extend(boardToVec(self.board))#78
		self.oppoBoard=_world.getOpponentPlayerBoard().getElements()
		self.retVec.extend(boardToVec(self.oppoBoard))#144
		self.hand=_world.getTurnPlayerHand().getElements()
		self.retVec.extend(handToVec(self.hand))#178
		self.oppohand=_world.getOpponentPlayerHand().getNumOfElements()
		self.retVec.extend(oppohandToVec(self.oppohand))#183
		return self.retVec
		pass
	def limitValue(self,_value,_min,_max):
		if _value<_min:
			return _min
			pass
		elif _value>_max:
			return _max
		else :
			return _value
		pass
class evolutioneryAgent(brain.baseBrain):
	"""docstring for evolutioneryAgent"""
	def __init__(self,_cardList,_rule):
		super(evolutioneryAgent, self).__init__(_cardList,_rule)
		self.numOfCandidates=16
		self.coefficients=[0 for i in range(5)]
		self.coefficients=self.developMutatedCoefficients()
		self.subCoefficients=self.developMutatedCoefficients()
		self.candidates=[0 for i in range(self.numOfCandidates)]
		self.historicCoefficients=[self.coefficients,self.subCoefficients]
	def developOwnDeck(self):
		self.retList=[]
		self.retList.append(copy.deepcopy(self.cardList[0]))
		self.retList.append(copy.deepcopy(self.cardList[0]))
		self.retList.append(copy.deepcopy(self.cardList[1]))
		self.retList.append(copy.deepcopy(self.cardList[1]))
		self.retList.append(copy.deepcopy(self.cardList[2]))
		self.retList.append(copy.deepcopy(self.cardList[2]))
		self.retList.append(copy.deepcopy(self.cardList[4]))
		self.retList.append(copy.deepcopy(self.cardList[4]))
		self.retList.append(copy.deepcopy(self.cardList[6]))
		self.retList.append(copy.deepcopy(self.cardList[6]))
		self.retList.append(copy.deepcopy(self.cardList[7]))
		self.retList.append(copy.deepcopy(self.cardList[7]))
		self.retList.append(copy.deepcopy(self.cardList[9]))
		self.retList.append(copy.deepcopy(self.cardList[10]))
		self.retList.append(copy.deepcopy(self.cardList[10]))
		self.retList.append(copy.deepcopy(self.cardList[13]))
		self.retList.append(copy.deepcopy(self.cardList[13]))
		self.retList.append(copy.deepcopy(self.cardList[14]))
		self.retList.append(copy.deepcopy(self.cardList[14]))
		self.retList.append(copy.deepcopy(self.cardList[15]))
		return self.retList
	def developMutatedCoefficients(self):
		self.retCoefficients=[random.random() for i in range(len(self.coefficients))]
		return self.normalizeCoefficients(self.retCoefficients)
	def developFluctuatedCoefficients(self,_coefficients,_maxFluctuation=0.1):
		self.tempCoefficients=copy.deepcopy(_coefficients)
		self.tempCoefficients=list(map(lambda i:i+((random.random()*2-1)*_maxFluctuation),self.tempCoefficients))
		return self.normalizeCoefficients(self.tempCoefficients)
		pass
	def normalizeCoefficients(self,_array):
		self.denominator=sum(_array)
		self.retArray=list(map(lambda i:i/self.denominator,_array))
		return self.retArray
		pass
	def evoluteCoefficients(self):
		self.coefficients,self.subCoefficients=self.optCoefficientsFromCandidates()
	def createNextGenerations(self):
		self.retCandidates=[]
		self.retCandidates.append(copy.deepcopy(self.coefficients))
		self.retCandidates.append(copy.deepcopy(self.subCoefficients))
		for i in range(int((self.numOfCandidates-4)/2)):
			self.retCandidates.append(self.developFluctuatedCoefficients(self.retCandidates[0]))
			self.retCandidates.append(self.developFluctuatedCoefficients(self.retCandidates[1]))
			pass
		self.retCandidates.append(self.developMutatedCoefficients())
		self.retCandidates.append(self.developMutatedCoefficients())
		return self.retCandidates
		pass
	def optCoefficientsFromCandidates(self):
		"""
		これまでの係数のプレイヤーと30回ずつ戦わせて、
		最も勝率の良かった係数を採用する。2番目のものはsubに。
		"""
		self.candidates=self.createNextGenerations()
		#self.winScore=[0 for i in range(self.numOfCandidates)]
		self.winScore=list(map(lambda item:self.getWinscore(item),self.candidates))
		self.coefficients=self.candidates[self.winScore.index(max(self.winScore))]
		self.maxValue=max(self.winScore)
		self.maxIndex=self.winScore.index(self.maxValue)
		self.subIndex=0
		self.subValue=0
		for i,item in enumerate(self.winScore):
			if self.subValue<item and i!=self.maxIndex :
				self.subValue=item
				self.subIndex=i
			pass
		return self.candidates[self.maxIndex],self.candidates[self.subIndex]
		pass
	def getWinscore(self,_coefficients):
		self.retScore=0
		for i in range(30):
			index=int(random.random()*len(self.historicCoefficients))
			self.agents=[coeffientPlayer(self.cardList,self.rule,_coefficients),coeffientPlayer(self.cardList,self.rule,self.historicCoefficients[index])]
			self.decks=[self.agents[0].developOwnDeck(),self.agents[1].developOwnDeck()]
			self.gm=gameMaster.gameMaster(self.decks)
			self.tree=self.gm.developInitialGameTree()
			self.retScore+=self.shift(self.tree)
			print(self.retScore)
			pass
		pass
	#def startBattle(self):

	#	pass
	def shift(self,_gameTree):
		if len(_gameTree.getMoves())==0:
			self.winnerIndex=self.gm.getWinnerIndex(_gameTree.getWorld())
			if self.winnerIndex==_gameTree.getWorld().getTurnPlayerIndex():
				return self.winnerIndex
			else:
				return 0
			pass
		self.command=self.chooseMoveByAI(_gameTree,self.agents[_gameTree.getWorld().getTurnPlayerIndex()])
		self.index=self.command["index"]
		self.moves=_gameTree.getMoves()
		return self.shift(self.gm.force(self.moves[self.index].getGameTreePromise()))
	def chooseMoveByAI(self,_gameTree,_agent):
		def fetchSimulationTrees(_moveTuple):
			self.retDict={
				"index":_moveTuple[0],
				"description":_moveTuple[1].getDescription(),
				"tree":_moveTuple[1].getSimulateTree(),
				}
			return self.retDict
			pass
		self.gmFor=gm.gmForAgent(_world=w.visibleWorld(_gameTree.getWorld()),_state=_gameTree.getState())
		self.state=_gameTree.getState()
		self.visibleWorld=w.visibleWorld(_gameTree.getWorld())
		self.simulationTrees=list(map(fetchSimulationTrees,enumerate(self.gmFor.getTree().getMoves())))
		#agentに選んでもらう
		self.m=_agent.chooseBestMove(self.visibleWorld,self.simulationTrees,self.state)
		return self.m
		pass
class coeffientPlayer(brain.baseBrain):
	"""docstring for coeffientPlayer"""
	def __init__(self,_cardList,_rule ,_coefficients=[0,0,0,0,0]):
		super(coeffientPlayer, self).__init__(_cardList,_rule)
		self.coefficients=_coefficients
	def chooseBestMove(self,_world,_moveList,_state):
		if len(_moveList)==1:
			return _moveList[0]
			pass
		self.index=0
		self.values=list(map(lambda m:self.getActionValue(_world,m["tree"],_description=m["description"]),_moveList))
		self.index=self.values.index(max(self.values))
		#print(self.values)
		return _moveList[self.index]
		pass
	def developOwnDeck(self):
		self.retList=[]
		self.retList.append(copy.deepcopy(self.cardList[0]))
		self.retList.append(copy.deepcopy(self.cardList[0]))
		self.retList.append(copy.deepcopy(self.cardList[1]))
		self.retList.append(copy.deepcopy(self.cardList[1]))
		self.retList.append(copy.deepcopy(self.cardList[2]))
		self.retList.append(copy.deepcopy(self.cardList[2]))
		self.retList.append(copy.deepcopy(self.cardList[4]))
		self.retList.append(copy.deepcopy(self.cardList[4]))
		self.retList.append(copy.deepcopy(self.cardList[6]))
		self.retList.append(copy.deepcopy(self.cardList[6]))
		self.retList.append(copy.deepcopy(self.cardList[7]))
		self.retList.append(copy.deepcopy(self.cardList[7]))
		self.retList.append(copy.deepcopy(self.cardList[9]))
		self.retList.append(copy.deepcopy(self.cardList[10]))
		self.retList.append(copy.deepcopy(self.cardList[10]))
		self.retList.append(copy.deepcopy(self.cardList[13]))
		self.retList.append(copy.deepcopy(self.cardList[13]))
		self.retList.append(copy.deepcopy(self.cardList[14]))
		self.retList.append(copy.deepcopy(self.cardList[14]))
		self.retList.append(copy.deepcopy(self.cardList[15]))
		return self.retList
	def getActionValue(self,_world,_move,_description=None):
		return self.simulateUntilEndOfMyTurn(_world,_move,_description=_description)
		pass
	def simulateUntilEndOfMyTurn(self,_world,_gameTreePromise,_description=None,_recursive=0):
		# return a value of board.
		# 自分の最後の盤面であればその時の評価値を返す。
		# それ以外であれば最大値を返す的な…
		self.nextTree=_gameTreePromise()
		if len(self.nextTree.getMoves())==0 or _recursive>5:
			return self.calculateWorldValue(_world)
			pass
		self.nextWorld=self.nextTree.getWorld()
		if self.nextWorld.getTurnPlayerIndex()!=_world.getTurnPlayerIndex():
			return self.calculateWorldValue(_world)
		return max(list(map(lambda m,w=self.nextWorld:self.simulateUntilEndOfMyTurn(w,m.getGameTreePromise(),_description=m.getDescription(),_recursive=_recursive+1),self.nextTree.getMoves())))
		pass
	def calculateWorldValue(self,_world):
		self.factors=[0 for i in range(len(self.coefficients))]
		self.opponentLife=_world.getOpponentPlayer().getLife()
		self.handValue=_world.getTurnPlayerHand().getNumOfElements()
		self.turnPlayerBoard=_world.getTurnPlayerBoard().getElements()
		self.boardValue=self.calculateBoardValue(self.turnPlayerBoard)
		self.opponentPlayerBoard=_world.getOpponentPlayerBoard().getElements()
		self.opponentBoardValue=self.calculateBoardValue(self.opponentPlayerBoard)
		self.currentMana=_world.getTurnPlayer().getCurrentMana()
		return sum(list(map(lambda item:self.factors[item[0]]*item[1],enumerate(self.coefficients))))
		pass
	def calculateBoardValue(self,_boardElements):
		return sum(list(map(lambda e:e.getCurrentPower(),_boardElements)))
		pass
	def getGameResult(self,_sign):
		self.arg=0
		if _sign:
			self.arg=1
			pass
		pass
