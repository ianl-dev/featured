## Game of Go project

**Purpose**: to build a machine-learned Go program 

**Reference material**: Deep Learning and the Game of Go (by Kevin Ferguson and Max Pumperla)

**Timeframe**: Jan 1st, 2020 - Feburary 2020 (ideal)

### How to play
1) Run the bot.v.bot.py file to have two bots playing against each other in randomized valid moves;
2) Run the human.v.bot file to play against a bot

### What is Go? 
One of the oldest and most complext board games in the world, Go originated in China around 3,000 years ago. 
It consists of a 19 by 19 board with two colors of stones: black and white. The game ends when both side passes,
or by resignation. The game play follows Japanese Go rule for simpler, more straightforward implementation.



### Key features
1) Go stones are structured in Gostring, where neighboring stones of the same color have a net liberty feature
2) Zobrist Hashing for easier manipulation and avoid recalculating hash values from scratch at every move
3) Naive bots' moves are randomized but valid. Later updates will make them smarter! Ko rule is also accounted.
