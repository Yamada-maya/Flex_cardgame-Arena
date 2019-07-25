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
### ルールについて(いつか英語にも対応させる)
- 各プレイヤーはライフとマナの2つのステータスを持ち、相手のライフが0になったプレイヤーが勝利する。
- 各プレイヤーはcardInformation.jsonの中から1種類につきmax_per_card(rule.jsonを参照)枚までカードを採用し、最低deck_min(rule.jsonを参照)枚のデッキを作成する
- デッキをよくシャッフルし、先行と後攻をランダムに決める。先行は手札を2枚デッキから引き、後攻は3枚引く。先攻がターンプレイヤーになる。
- 以下をどちらかのプレイヤーのライフが0になるまで繰り返す。
	1. ターンプレイヤーの場にあるすべてのカードを未行動にし、カードを1枚引く。マナがmax_mana(rule.jsonを参照)でなかった場合、マナを1増やして全回復する。
	2. 以下の行動を可能な限り何度でも行ってよい。
		- 手札のカードをマナを支払うことでプレイする。そのカードのカードタイプがクリーチャーであった場合そのクリーチャーがターンプレイヤーの場に現れ、ソーサリーであった場合そのカードの効果が及ぼされる。
		- 場にあるクリーチャーを行動済みにすることで相手の場にあるカード、もしくは相手を攻撃する。クリーチャーを攻撃した場合、お互いのクリーチャーのtoughnessが相手のpower分だけ減る。toughnessが0になったクリーチャーは墓地に送られる。
		- 場にあるカードの起動型スキルを起動する。
	3. ターンを終了する。ターンプレイヤーが移る。