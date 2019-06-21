# カードゲームの実装、GUIとともに
# 動作確認のため、いろいろと可視化できるようにする
# 右下にstepボタンを用意、押すと展開が進むようにする
# gameMaster classを保持。ボタンを押すごとにgameMasterが次のノードを返す。
# そのノードを基にApplication classが描画
# main class は主に描画担当
import sys
import tkinter as tk
import gameMaster as gm
import gmForAgent
import copy
import deckBuilder as db
import brain
import myAgent
import world as w
import time as t
import json
import datetime
class human(object):
	"""docstring for human"""
	def __init__(self):
		super(human, self).__init__()
		pass
		
class visualizeApp(tk.Tk):
	def __init__(self):
		tk.Tk.__init__(self)
		# カード情報やルールのインポート
		self.f = open('data/cardInformation.json', 'r')
		self.cardList=json.load(self.f)
		self.f.close()
		self.f=open('data/rule.json', 'r')
		self.rule=json.load(self.f)
		self.f.close()
		# ここまで
		self.geometry("800x600")
		self.grid_rowconfigure(0, weight=1)
		self.grid_columnconfigure(0, weight=1)
		self.deckEditFrame=db.deckBuilder(self.cardList,self.rule,master=self)
		#self.battleFrame=tk.Frame(self)
		#self.battleFrame.place(relx=0,rely=0,relwidth=1,relheight=1)
		self.deckEditFrame.tkraise()
		self.agents=[human(),brain.ruleBaseBrain()]
		self.rightDeck=[]
		self.leftDeck=[]
		self.iterate=0
		while not self.doesDeckSuitForRules(self.rightDeck,self.cardList,self.rule):
			if self.iterate==5:
				print("error")
				sys.exit(self.iterate)
				pass
			self.rightDeck=self.agents[1].developOwnDeck(copy.deepcopy(self.cardList),copy.deepcopy(self.rule))
			self.iterate+=1
			pass
		if isinstance(self.agents[0],human):
			self.createDeckEditWindow()
		else:
			self.iterate=0
			while not self.doesDeckSuitForRules(self.leftDeck,self.cardList,self.rule):
				if self.iterate==5:
					sys.exit(self.iterate)
					pass
				self.leftDeck=self.agents[0].developOwnDeck(copy.deepcopy(self.cardList),copy.deepcopy(self.rule))
				self.iterate+=1
				pass
			self.changeBattlePage()

	def createDeckEditWindow(self):
		self.deckEditFrame.place(relx=0,rely=0,relwidth=1,relheight=1)
		pass
	def createConfirmWindow(self):
		self.leftDeck=self.deckEditFrame.getDeckList()
		self.confirmFrame=tk.Frame(self)
		self.confirmFrame.place(relx=0,rely=0,relwidth=1,relheight=1)
		self.confirmButton=tk.Button(self.confirmFrame,text="start game",command=self.changeBattlePage)
		self.confirmButton.place(relx=0.5,rely=0.5,relwidth=0.5,relheight=0.5)
		pass
	def changeBattlePage(self):
		self.confirmFrame.place_forget()
		self.moveButton=[]
		self.gm=gm.gameMaster([self.leftDeck,self.rightDeck])
		self.tree=self.gm.developInitialGameTree()
		self.visualizeFirstNode(self.tree.getWorld())
		self.after(100,lambda:self.shift(self.tree))
		pass
	def doesDeckSuitForRules(self,_deck,_cardList,_rule):
		self.checkDict={}
		for item in _deck:
			if not (item in _cardList):
				return False
			else:
				if item["cardName"] in self.checkDict.keys():
					self.checkDict[item["cardName"]]+=1
					pass
				else:
					self.checkDict[item["cardName"]]=1
				pass
			pass
		for key in self.checkDict.keys():
			if self.checkDict[key]>_rule["max_per_card"]:
				return False
				pass
			pass
		if sum(list(map(lambda k:self.checkDict[k],self.checkDict.keys())))<_rule["deck_min"]:
			return False
			pass
		return True
		pass
	def shift(self,_gameTree):
		if len(_gameTree.getMoves())==0:
			sys.exit()
			pass
		self.visualizeMatchFromNode(_gameTree.getWorld())
		if isinstance(self.agents[_gameTree.getWorld().getTurnPlayerIndex()],human):
			self.setUpUI(_gameTree)
			pass
		else:
			self.command=self.chooseMoveByAI(_gameTree,self.agents[_gameTree.getWorld().getTurnPlayerIndex()])
			self.moves=_gameTree.getMoves()
			print("thinking time....-----------------------")
			self.after(1000,lambda:self.shift(self.gm.force(self.moves[self.command["index"]].getGameTreePromise())))
		pass
	def chooseMoveByAI(self,_gameTree,_agent):
		t.sleep(0.1)
		print("waiting...")
		def fetchSimulationTrees(_moveTuple):
			self.retDict={
				"index":_moveTuple[0],
				"description":_moveTuple[1].getDescription(),
				"tree":_moveTuple[1].getSimulateTree(),
				}
			return self.retDict
			pass
		self.moves=_gameTree.getMoves()
		self.state=_gameTree.getState()
		self.visibleWorld=w.visibleWorld(_gameTree.getWorld())
		self.simulationTrees=list(map(fetchSimulationTrees,enumerate(self.moves)))
		#agentに選んでもらう
		self.m=_agent.chooseBestMove(self.visibleWorld,copy.deepcopy(self.simulationTrees),self.state)
		return self.m
		pass
	def visualizeFirstNode(self,_world):
		self.leftUnit=[]
		self.rightUnit=[]
		self.leftHand=[]
		self.players=_world.getPlayers()
		self.decks=_world.getDecks()
		self.leftLifeArea=tk.Label(self,text="Life point:{life}".format(life=self.players[0].getLife()))
		self.leftLifeArea.place(relx=0,rely=0,relwidth=0.5,relheight=0.1)
		self.leftHandArea=tk.Label(self,text="hand Area")
		self.leftHandArea.place(relx=0,rely=0.2,relwidth=0.2,relh=0.7)
		self.leftDeckArea=tk.Button(self,text="deck left:{numOfDeck}".format(numOfDeck=self.decks[0].getNumOfElements()))
		self.leftDeckArea.place(relx=0.2,rely=0.1,relwidth=0.3,relheight=0.1)
		self.leftManaArea=tk.Label(self,text="You have 0 mana.")
		self.leftManaArea.place(relx=0,rely=0.1,relwidth=0.2,relheight=0.1)
		self.leftUnitArea=tk.Button(self,text="cost:\ntoughness:\npower:")
		self.leftUnitArea.place(relx=0.2,rely=0.2,relwidth=0.3,relheight=0.8)
		self.rightHandArea=tk.Label(self,text="hand Area")
		self.rightHandArea.place(relx=0.8,rely=0.2,relwidth=0.2,relheight=0.7)
		self.rightDeckArea=tk.Button(self,text="deck left:{numOfDeck}".format(numOfDeck=self.decks[1].getNumOfElements()))
		self.rightDeckArea.place(relx=0.5,rely=0.1,relwidth=0.3,relheight=0.1)
		self.rightManaArea=tk.Label(self,text="You have 0 mana.")
		self.rightManaArea.place(relx=0.8,rely=0.1,relwidth=0.2,relheight=0.1)
		self.rightLifeArea=tk.Label(self,text="Life point:{life}".format(life=self.players[1].getLife()))
		self.rightLifeArea.place(relx=0.5,rely=0,relwidth=0.5,relheight=0.1)
		self.rightUnitArea=tk.Button(self,text="cost:\ntoughness:\npower:")
		self.rightUnitArea.place(relx=0.5,rely=0.2,relwidth=0.3,relheight=0.8)
		pass
	def visualizeMatchFromNode(self,_world):
		self.forgetAllArea()
		self.players=_world.getPlayers()
		self.hands=_world.getHands()
		self.decks=_world.getDecks()
		self.boards=_world.getBoards()
		self.leftLifeArea=tk.Label(self,text="Life point:{life}".format(life=self.players[0].getLife()))
		self.leftLifeArea.place(relx=0,rely=0,relwidth=0.5,relheight=0.1)
		self.leftHand=[]
		for i,item in enumerate(self.hands[0].getElements()):
			self.leftHand.append(tk.Button(self,text="{card}".format(card=item.getCardName())))
			self.leftHand[i].place(relx=0,rely=0.2+0.7*i/self.hands[0].getNumOfElements(),relwidth=0.2,relheight=0.7/self.hands[0].getNumOfElements())
			pass
		#self.leftHandArea=tk.Label(self,text="hand Area")
		#self.leftHandArea.place(relx=0,rely=0.2,relwidth=0.2,relh=0.7)
		self.leftDeckArea=tk.Button(self,text="deck left:{numOfDeck}".format(numOfDeck=self.decks[0].getNumOfElements()))
		self.leftDeckArea.place(relx=0.2,rely=0.1,relwidth=0.3,relheight=0.1)
		self.leftManaArea=tk.Label(self,text="You have {mana} mana.".format(mana=self.players[0].getCurrentMana()))
		self.leftManaArea.place(relx=0,rely=0.1,relwidth=0.2,relheight=0.1)
		self.leftUnit=[]
		for i,item in enumerate(self.boards[0].getElements()):
			self.leftUnit.append(tk.Label(self,text="Name={name}\nCost={cost}\nPower={power}\nToughness={toughness}\nstand={isStand}".format(name=item.getCardName(),cost=item.getCurrentCost(),power=item.getCurrentPower(),toughness=item.getCurrentToughness(),isStand=item.isStand())))
			self.leftUnit[i].place(relx=0.2,rely=0.2+0.2*i,relwidth=0.3,relheight=0.2)
			pass
		self.rightUnit=[]
		for i,item in enumerate(self.boards[1].getElements()):
			self.rightUnit.append(tk.Label(self,text="Name={name}\nCost={cost}\nPower={power}\nToughness={toughness}\nstand={isStand}".format(name=item.getCardName(),cost=item.getCurrentCost(),power=item.getCurrentPower(),toughness=item.getCurrentToughness(),isStand=item.isStand())))
			self.rightUnit[i].place(relx=0.5,rely=0.2+0.2*i,relwidth=0.3,relheight=0.2)
			pass
		#self.leftUnitArea=tk.Button(self,text="cost:\ntoughness:\npower:")
		#self.leftUnitArea.place(relx=0.2,rely=0.2,relwidth=0.3,relheight=0.8)
		self.rightHandArea=tk.Label(self,text="{num}".format(num=self.hands[1].getNumOfElements()))
		self.rightHandArea.place(relx=0.8,rely=0.2,relwidth=0.2,relheight=0.7)
		self.rightDeckArea=tk.Button(self,text="deck left:{numOfDeck}".format(numOfDeck=self.decks[1].getNumOfElements()))
		self.rightDeckArea.place(relx=0.5,rely=0.1,relwidth=0.3,relheight=0.1)
		self.rightManaArea=tk.Label(self,text="You have {mana} mana.".format(mana=self.players[1].getCurrentMana()))
		self.rightManaArea.place(relx=0.8,rely=0.1,relwidth=0.2,relheight=0.1)
		self.rightLifeArea=tk.Label(self,text="Life point:{life}".format(life=self.players[1].getLife()))
		self.rightLifeArea.place(relx=0.5,rely=0,relwidth=0.5,relheight=0.1)
		#self.rightUnitArea=tk.Button(self,text="cost:\ntoughness:\npower:")
		#self.rightUnitArea.place(relx=0.5,rely=0.2,relwidth=0.3,relheight=0.8)
		pass
	def setUpUI(self,_gameTree):
		"""
		ボタン式UIにする。やっぱりフェーズに合わせてって感じになるんかな？
		stepは何も選ばず次のフェーズへ、ボタン式UIは選んで行動。という感じで…
		REMARK!!!:AIの行動の時はここをstepだけにする。
		"""
		self.moves=_gameTree.getMoves()
		self.moveButton=[]
		self.move=[]
		for i,m in enumerate(self.moves):
			self.move.append(copy.deepcopy(m))
			self.moveButton.append(tk.Button(self,text=self.move[i].getDescription(),command=lambda index=i:self.shift(self.gm.force(self.move[index].getGameTreePromise()))))
			self.moveButton[i].place(relx=i/len(self.moves),rely=0.9,relwidth=1/len(self.moves),relheight=0.1)
			pass
	def forgetAllArea(self):
		self.leftLifeArea.place_forget()
		self.leftUnitArea.place_forget()
		self.leftManaArea.place_forget()
		self.leftHandArea.place_forget()
		self.leftDeckArea.place_forget()
		self.rightLifeArea.place_forget()
		self.rightUnitArea.place_forget()
		self.rightManaArea.place_forget()
		self.rightHandArea.place_forget()
		self.rightDeckArea.place_forget()
		for item in self.leftUnit:
			item.place_forget()
			pass
		for item in self.rightUnit:
			item.place_forget()
			pass
		for item in self.leftHand:
			item.place_forget()
			pass
		for item in self.moveButton:
			item.place_forget()
		pass
class simpleApp(object):
	"""docstring for simpleApp"""
	def __init__(self):
		super(simpleApp, self).__init__()
		self.f = open('data/cardInformation.json', 'r')
		self.cardList=json.load(self.f)
		self.f.close()
		self.f=open('data/rule.json', 'r')
		self.rule=json.load(self.f)
		self.f.close()
		# ここまで
		self.agents=[brain.ruleBaseBrain(),brain.ruleBaseBrain()]
		self.rightDeck=[]
		self.leftDeck=[]
	def deckBuild(self):
		self.iterate=0
		while not self.doesDeckSuitForRules(self.rightDeck,self.cardList,self.rule):
			if self.iterate==5:
				print("error")
				sys.exit(self.iterate)
				pass
			self.rightDeck=self.agents[1].developOwnDeck(copy.deepcopy(self.cardList),copy.deepcopy(self.rule))
			self.iterate+=1
			pass
		self.iterate=0
		while not self.doesDeckSuitForRules(self.leftDeck,self.cardList,self.rule):
			if self.iterate==5:
				sys.exit(self.iterate)
				pass
			self.leftDeck=self.agents[0].developOwnDeck(copy.deepcopy(self.cardList),copy.deepcopy(self.rule))
			self.iterate+=1
			pass
		pass
	def doesDeckSuitForRules(self,_deck,_cardList,_rule):
		self.checkDict={}
		for item in _deck:
			if not (item in _cardList):
				return False
			else:
				if item["cardName"] in self.checkDict.keys():
					self.checkDict[item["cardName"]]+=1
					pass
				else:
					self.checkDict[item["cardName"]]=1
				pass
			pass
		for key in self.checkDict.keys():
			if self.checkDict[key]>_rule["max_per_card"]:
				return False
				pass
			pass
		if sum(list(map(lambda k:self.checkDict[k],self.checkDict.keys())))<_rule["deck_min"]:
			return False
			pass
		return True
		pass
	def giveResult(self,_world,_agentTuple):
		self.winnerIndex=self.gm.getWinnerIndex(_world)
		self.sign=self.winnerIndex==_agentTuple[0]
		_agentTuple[1].getGameResult(self.sign)
		if self.sign:
			numOfWin[_agentTuple[0]]+=1
			pass
		pass
	def shift(self,_gameTree):
		print(type(_gameTree.getWorld()))
		if len(_gameTree.getMoves())==0:
			_gameTree.getWorld().dumpWorld()
			l=list(map(lambda agent:self.giveResult(_gameTree.getWorld(),agent),enumerate(self.agents)))
			return
			pass
		self.command=self.chooseMoveByAI(_gameTree,self.agents[_gameTree.getWorld().getTurnPlayerIndex()])
		self.index=self.command["index"]
		self.moves=_gameTree.getMoves()
		print("------------------current world is...------------------")
		_gameTree.getWorld().dumpWorld()
		print("------------------end---------------------")
		print("you can...")
		for item in self.moves:
			print(item.getDescription())
			pass
		print("you chose->")
		print(self.moves[self.index].getDescription())
		self.shift(self.gm.force(self.moves[self.index].getGameTreePromise()))
	def chooseMoveByAI(self,_gameTree,_agent):
		t.sleep(0.1)
		def fetchSimulationTrees(_moveTuple):
			self.retDict={
				"index":_moveTuple[0],
				"description":_moveTuple[1].getDescription(),
				"tree":_moveTuple[1].getSimulateTree(),
				}
			return self.retDict
			pass
		self.gmFor=gmForAgent.gmForAgent(_world=w.visibleWorld(_gameTree.getWorld()),_state=_gameTree.getState())
		#self.argMoves=_gameTree.getMoves()
		self.state=_gameTree.getState()
		self.visibleWorld=w.visibleWorld(_gameTree.getWorld())
		self.simulationTrees=list(map(fetchSimulationTrees,enumerate(self.gmFor.getTree().getMoves())))
		#agentに選んでもらう
		self.m=_agent.chooseBestMove(self.visibleWorld,self.simulationTrees,self.state)
		return self.m
		pass
	def startBattle(self):
		self.deckBuild()
		self.gm=gm.gameMaster([self.leftDeck,self.rightDeck])
		self.tree=self.gm.developInitialGameTree()
		self.shift(self.tree)
		pass

def main(_visualize=False):
	if _visualize:
		app=visualizeApp()
		app.mainloop()
		pass
	else:
		app=simpleApp()
		print(datetime.datetime.now())
		for i in range(1):
			app.startBattle()
			print(datetime.datetime.now())
			print(numOfWin)

	pass
if __name__ == '__main__':
	numOfWin=[0,0]
	main()
