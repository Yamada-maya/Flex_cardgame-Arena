# Flex_cardgame-Arena
### What is this?
- This is platform for developing agents of Trading Card Game (TCG) written in python by Yamada-maya.
### Can I contribute?
- Sure! 
- There are a lot to do.
### Project structure

```
ver_alpha
├── brain.py // This file includes agents' brain. You can develop original agents by inheritting "baseBrain" class .
├── cardInformation.py
├── deckBuilder.py
├── gameMaster.py   // Game source code.
├── gameTree.py
├── main.py    // Application UI code and organize.
├── move.py
├── playerAttributes.py
└── data  // Cards, rule data are included.
```

### How to develop brain.py
- brain has two roles.
	- as a builder of decks
	- as a agent of games
- We are implementing deck building part.
- In the game, chooseBestMove function should be implemented to develop original agent. In chooseBestMove function, brain class must return one "move" from "_moveList" ("_moveList" is argment for chooseBestMove function).
	- By executing _moveList["tree"], you can get next "gameTree". ( _moveList["tree"]() returns "gameTree" class which includes "move", "world").