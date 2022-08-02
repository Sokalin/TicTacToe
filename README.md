# TicTacToe
<h3>How it use</h3>
<p>
<strong>Firstly</strong> you should create object of class TicTacToe
You can take 3 args:
<br>
amount rows of game field, amout colums and amount chars for win (all args by default equls 3)
</p>
<code>game = TicTacToe(rows=3, cols=5, win_am=2)</code>
<br>or<br>
<code>game = TicTacToe()</code> <i>rows=3, cols=3, win_am=3</i>
<p><br>
<strong>Secondly</strong> you should create some players:
</p>
<code>game.create_player('A', 'h', 'name')</code><br>
<code>game.create_player('B', 'c', 'name')</code><br>
<code>game.create_player('C', 'h')</code><br>
<code>...............................</code><br>
Here first arg is unique symbol (two players musn't have one symbol).<br>
Secod arg is type of player: h - human (for move player must be input index in console), c - computer (move by using random).<br>
Third arg is name of player: you can create player without name, it use for view in console.<br><br>
<strong>Then</strong> you can call method play:<br>
<code>game.play()</code><br>
It begins the game in console with all created players. If you want start game with correct players you can give there chars to method play:<br>
<code>game.play('A', 'C')</code><br>
You can call this method as many times as you like.<br><br>
If you want change game field size between games your can use specific method:<br>
<code>game.change_size(3, 4, 3)game.play('A', 'C')</code><br>
There are args like in initioin game object.
