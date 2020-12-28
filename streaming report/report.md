[TOC]



# Get live game statistics using spark streaming	

## Goal

The main goal of this task is to find a way to predict the game results given the player games statistics before entering the game. In addition , we try to find out the threat player in each team so  that the other team can focus the attacks on him.

## Used APIs

* We have used [Riot APIs](https://developer.riotgames.com/) which gives us live data of games in addition to giving us helpful information about each summoner's playing history.
* Riot games gives us 20 API calls per second and and 100 API calls per two minutes for each region. Hence the data querying was very limited.
* In order to best utilize the API calls we tried to ultimate between regions , but for some reason some summoners couldn't be found within the same region and we couldn't have time to trace back that behavior.
* the used APIs from the website are as  follows:
  1. [Featured games-v4 : this API is within the spectator section which gives you a list of games being played live within the specified region.
  2. Summoner-V4: this API contains the list of data for each each spectator such as summoner ID , account ID and more.
  3. Champion mastery-V4: this API gives you the performance of a specific summoner with a specific champion. the statistics contains the most recent time this player summoned this champion , champion level and champion score.
  4. Match-V4 : this gives a list of matches played by a summoner. In addition it can give you detailed statistics on the performance of that player in that match.

* We did use the match API on a single player to get more complex heuristic function but the main problem is that it's costly in th amount of API calls needed as you make a call per game played per player and no matter how small the amount of matches per player will be , it will eventually get multiplied by 10 (the number of players).Hence, we chose not to use it in the final heuristic and only use champion mastery in order to get get the score for each user.

## How to get game probability and most threat

The threat and score are both entangled with the same heuristic function and the steps to get them are as follows:

For each player in the team :

1. calculate the score 
2. find whether it's the maximum of its team or not 
3. if it is then update the team threat player as the current one .
4. add the player score too the rest of players scores.

After getting done do the apply the following formula to get the team chance of winning:
$$
winProbability =  \frac{Team Score}{Sum Of Two Teams Score}
$$


## Heuristic function 

* the heuristic function utilized the only three parameters that won't be costly to fetch for each user. and these are as follows : 
  1. champion familiarity: and this is calculated by subtracting the current time for the last time the player used this champion , which  will give us an insight on how familiar this player with that champion (the smaller the number the better).
  2. champion Level : Each champion has a global level that goes from 1 to 7 and then it stops  , which tells on how frequent and experienced this player with that champion.
  3. champion Points: this represent the number of points the champion have for that player.

* we have used multiple heuristics and tried to get see which one will work optimally with the data we have as we  have collected some games and predicted the output, then we waited for the games to end to know which one matched the statics of ours.

* the main heuristics are similar but with different philosophies. The first one just multiples the champion points and levels and then divide it over champion familiarity as follows:

  
  $$
  Score_1=  \frac{chajm points \times Champion level}{ChampFamiliarity}
  $$

* Although this heuristic seems logical , but naturally, human don't have a linear skill development, rather we have logarithmic one , meaning that if my score jumped from 1000 to 10000 this does not mean that my performance in the game has jumped to 10 folds of the  oldest one

* the same argument can be made with champion familiarity as the familiarity with the champion almost asymptotes with the development of time.

* Thus we made different heuristic to see which one will perform better and whether our reasoning is sound or not. The next one is just logging the numerator and the denominator and divide them over each other as follows

  
  $$
  Score_2 =  \frac{\ln(chajm points \times Champion level)}{\ln(ChampFamiliarity)}
  $$

* For completeness we tried to just log the denominator and leave the upper score as it is and see , as  we have speculated that maybe the game itself has incorporated this skill logarithmic assumption in the score and made it harder to go from one level to the other making the assumption we had before invalid.
  $$
  Score_3 =  \frac{chajm points \times Champion level}{\ln(ChampFamiliarity)}
  $$

* 

# Results 

* The results has been calculated by acquiring the results of 30 similar matches and comparing the team probability of winning with the team prediction. We calculated the number of correct guesses over the total number for each team to see the performance of the three heuristics.

* As it can be seen The Accuracy o heuristic 2 reaches over 60% accuracy.

* it's noted that the accuracy of blue is always less than the red team with a big margin. Maybe the game meant to do that to make the oppsing team always a little bit challenging to the current team, but further investigation with bigger data needs to be made.

* with such simple heuristics we could predict with decent accuracy the percentage of winning for each team. 

* This problem is challenging because Mostly the game tries to balance the teams level not to make it boring for both of them and keep it always interesting.

  ![chart](/mnt/MY_FILES/ZC/Year_5/Fall_2020/BigData/Spark/chart.jpg)
