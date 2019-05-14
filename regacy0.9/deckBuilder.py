import json
import tkinter as tk
import copy
#デッキビルドAIをここに組み込むか。
class deckBuilder(tk.Frame):
	"""docstring for deckBuilder"""
	def __init__(self,master=None):
		tk.Frame.__init__(self,master,width=640,height=480)
		self.master=master
		self.pack()
		self.f = open('data/cardInformation.json', 'r')
		self.cardList=json.load(self.f)
		self.f.close()
		self.f=open('data/rule.json', 'r')
		self.rule=json.load(self.f)
		print(self.rule)
		self.f.close()
		self.index=0
		self.cardLimit=self.rule["max_per_card"]
		self.deckMin=self.rule["deck_min"]
		self.isDeckBuilt=False
		self.deckList=[]
		self.numOrganizer=[0 for i in range(len(self.cardList))]
		self.developDeckbuildWindow()
	def deckCreate(self):
		if self.calculateDeckSum()>=self.deckMin:
			self.isDeckBuilt=True
			for i,item in enumerate(self.numOrganizer):
				for x in range(item):
					self.appendCard=copy.deepcopy(self.cardList[i])
					self.deckList.append(self.appendCard)
					pass
				pass
			self.master.destroy()
			pass
		pass
	def getDeckList(self):
		return self.deckList
		pass
	def shiftLeft(self):
		self.index-=1
		self.index%=len(self.cardList)
		pass
	def shiftRight(self):
		self.index+=1
		self.index%=len(self.cardList)
		pass
	def adoptCard(self):
		if self.numOrganizer[self.index]<self.cardLimit:
			self.numOrganizer[self.index]+=1
		pass
	def denyCard(self):
		if self.numOrganizer[self.index]>0:
			self.numOrganizer[self.index]-=1
			pass
		pass
	def commanded(self,_state):
		if _state=="shiftLeft":
			self.shiftLeft()
			pass
		if _state=="shiftRight":
			self.shiftRight()
			pass
		if _state=="adopt":
			self.adoptCard()
			pass
		if _state=="deny" :
			self.denyCard()
			pass
		if _state=="finish":
			self.deckCreate()
			pass
		if not self.isDeckBuilt:
			self.developDeckbuildWindow()
			pass
		pass
	def developDeckbuildWindow(self):
		#デッキ作成画面。mtgAのような画面でいいかな？
		self.leftFocusedCard=tk.Label(self,text=self.cardInfoToStr(self.cardList[(self.index-1)%len(self.cardList)]))
		self.focusedCard=tk.Label(self,text=self.cardInfoToStr(self.cardList[self.index%len(self.cardList)]))
		self.rightFocusedCard=tk.Label(self,text=self.cardInfoToStr(self.cardList[(self.index+1)%len(self.cardList)]))
		self.leftShiftButton=tk.Button(self,text="shift to\nprevious card",command=lambda state="shiftLeft":self.commanded(state))
		self.rightShiftButton=tk.Button(self,text="shift to\nnext card",command=lambda state="shiftRight":self.commanded(state))
		self.adoptButton=tk.Button(self,text="adopt this card",command=lambda state="adopt":self.commanded(state))
		self.denyButton=tk.Button(self,text="deny this card",command=lambda state="deny":self.commanded(state))
		self.decideDeckButton=tk.Button(self,text="decide your deck",command=lambda state="finish":self.commanded(state))
		self.leftShiftButton.place(relx=0,rely=0,relwidth=0.1,relheight=0.9)
		self.rightShiftButton.place(relx=0.5,rely=0,relwidth=0.1,relheight=0.9)
		self.leftFocusedCard.place(relx=0.1,rely=0.5,relwidth=0.1,relheight=0.4)
		self.rightFocusedCard.place(relx=0.4,rely=0.5,relwidth=0.1,relheight=0.4)
		self.focusedCard.place(relx=0.2,rely=0.3,relwidth=0.2,relheight=0.6)
		self.adoptButton.place(relx=0,rely=0.9,relwidth=0.3,relheight=0.1)
		self.denyButton.place(relx=0.3,rely=0.9,relwidth=0.3,relheight=0.1)
		self.decideDeckButton.place(relx=0.6,rely=0.9,relwidth=0.4,relheight=0.1)
		self.currentDeck=tk.Label(self,text=self.deckListToStr())
		self.currentDeck.place(relx=0.6,rely=0,relwidth=0.4,relheight=0.9)
		pass
	def cardInfoToStr(self,cardInformation):
		self.retStr="CardName:{name}\n".format(name=cardInformation["cardName"])
		self.retStr+="Cost:{cost}\n".format(cost=cardInformation["baseCost"])
		self.retStr+="Toughness:{toughness}\n".format(toughness=cardInformation["baseToughness"])
		self.retStr+="Power:{power}\n".format(power=cardInformation["basePower"])
		self.retStr+="Type:{type}".format(type=cardInformation["cardType"]["main"])
		return self.retStr
		pass
	def deckListToStr(self):
		self.retStr=""
		for i,item in enumerate(self.cardList):
			if self.numOrganizer[i]>0:
				self.retStr+="{num}:{cardName}\n".format(num=self.numOrganizer[i],cardName=item["cardName"])
				pass
			pass
		return self.retStr
		pass
	def calculateDeckSum(self):
		return sum(self.numOrganizer)
		pass
