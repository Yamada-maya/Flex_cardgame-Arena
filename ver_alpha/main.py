# カードゲームの実装、GUIとともに
# 動作確認のため、いろいろと可視化できるようにする
# 右下にstepボタンを用意、押すと展開が進むようにする
# gameMaster classを保持。ボタンを押すごとにgameMasterが次のノードを返す。
# そのノードを基にApplication classが描画
# main class は主に描画担当
import tkinter as tk
import gameMaster as gm
import copy
import deckBuilder as db
import brain
import world as w
import time as t
import json
class human(object):
	"""docstring for human"""
	def __init__(self):
		super(human, self).__init__()
		
class Application(tk.Frame):
	def __init__(self, master=None,_deckListL=[],_deckListR=[]):
		tk.Frame.__init__(self, master,width=640,height=480)
		self.pack()
		self.moveButton=[]
		self.agents=[human(),brain.randomBrain()]
		self.gm=gm.gameMaster([_deckListL,_deckListR])
		self.tree=self.gm.developInitialGameTree()
		self.visualizeFirstNode(self.tree.getWorld())
		self.after(100,lambda:self.shift(self.tree))

	def shift(self,_gameTree):
		self.visualizeMatchFromNode(_gameTree.getWorld())
		if isinstance(self.agents[_gameTree.getWorld().getTurnPlayerIndex()],human):
			self.setUpUI(_gameTree)
			pass
		else:
			self.command=self.chooseMoveByAI(_gameTree,self.agents[_gameTree.getWorld().getTurnPlayerIndex()])
			self.moves=_gameTree.getMoves()
			self.after(500,lambda:self.shift(self.gm.force(self.moves[self.command["index"]].getGameTreePromise())))
		pass
	def chooseMoveByAI(self,_gameTree,_agent):
		t.sleep(0.1)
		print("waiting...")
		def fetchSimulationTrees(_moveTuple):
			self.retDict={
				"index":_moveTuple[0],
				"description":_moveTuple[1].getDescription(),
				"tree":_moveTuple[1].getSimulateTree()}
			return self.retDict
			pass
		self.moves=_gameTree.getMoves()
		if len(self.moves)==1:
			self.retMove=fetchSimulationTrees((0,self.moves[0]))
			return self.retMove
		self.visibleWorld=w.visibleWorld(_gameTree.getWorld())
		self.simulationTrees=list(map(fetchSimulationTrees,enumerate(self.moves)))
		#agentに選んでもらう
		self.m=_agent.chooseBestMove(self.visibleWorld,self.simulationTrees)
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
		if len(_gameTree.getMoves())==1 and _gameTree.getMoves()[0].getGameTreePromise() is None:
			self.move=_gameTree.getMoves()
			self.moveButton=[]
			self.moveButton.append(tk.Button(self,text=self.move[0].getDescription(),command=lambda :self.shift(self.gm.developInitialGameTree())))
			self.moveButton[0].place(relx=0,rely=0.9,relwidth=1,relheight=0.1)
			pass
		else:
			self.moves=_gameTree.getMoves()
			self.moveButton=[]
			self.move=[]
			for i,m in enumerate(self.moves):
				self.move.append(copy.deepcopy(m))
				self.moveButton.append(tk.Button(self,text=self.move[i].getDescription(),command=lambda index=i:self.shift(self.gm.force(self.move[index].getGameTreePromise()))))
				self.moveButton[i].place(relx=i/len(self.moves),rely=0.9,relwidth=1/len(self.moves),relheight=0.1)
				pass
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
if __name__ == '__main__':
	dbRoot=tk.Tk()
	deckWindow=db.deckBuilder(master=dbRoot)
	deckWindow.mainloop()
	deck=deckWindow.getDeckList()
	gameRoot = tk.Tk()
	app = Application(master=gameRoot,_deckListL=deck,_deckListR=deck)
	app.mainloop()
