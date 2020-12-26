# Reading this [document](https://docs.google.com/document/d/1ZlHqpx2XVmqZp_9CGoD7EcOZd39Gd73oTEILJnztpxI/edit)

## Initial thoughts
given what I have seen on Kaggle sample json objects

#### I Champion win, pick, and ban rates [^1]
- win --> easy
- pick -> how many times it was used across the games
- confused about ban (what is pickTurn and where to find ban)

#### II Champion Synergies or duos 
- what I have in mind is is to do nxn matrix displaying how many times each champion was duoed with another champion [^2]
- check win rate (common win rate) 5c2 permutations (pick and win-rate bl tuple) order alphabitically
- just output relation like champion-1 champion-2 \

champion4 - champion7 and so on

#### III Item win, pick rates
- for pick rates just count how many times it was picked over the whole dataset and how many times it was with the win and lost with (If I am understanding correctly) sampe

#### III Item win, pick rates (There are restrictions on items check the video)
To build the matrix use the constant files Eng. Ahmed talked about
- n x d matrix where n is the number of champions d is the number of items in the game


#### IV Item Synergies (item with champion, item with class) (bonus if per patch) (pick win - rate)
To build the matrix use the constant files Eng. Ahmed talked about
- n x d matrix where n is the number of champions d is the number of items in the game
- n x c matrix where n is the number of champions c is the number of classes

#### V Item suggestions
So the objective is to find the most fit items for each champion (but what makes this different than synergies)

no mythic - no starter

basic - epic - (legendary)  suggest 6 legendary items (one of them shoes - pick win rate) given class champion (pick - win rate with champion)
first 3 items (generic) 1 of them is shoes (except kathipia)
matchup (vs )

evolve_into nothing



#### VI [Streaming] Win prediction for live matches
- which team will win the game
- Don't know what to do to be honest
- mostly something that has to do with kill-rate stats in general
- Check **timeline** as it shows gold per Min / xp diff / damage taken


#### VII [Streaming] Threat prediction for live matches
- which of the 5 players is the real threat
- Don't know what to do to be honest
- mostly something that has to do with kill-rate stats in general
- Check **timeline** as it shows gold per Min / xp diff / damage taken





## 
rank games (Draft pick)

## to reach specific fields
[^1]: to reach participants:  participants -> stats
ban: can be found in teams --> 0 or 1 (which team) -> bans --> 0 to 5

[^2]: wto find items used by each participant: participants -> stats -> item 0-9 -> name

