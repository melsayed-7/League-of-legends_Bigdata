import findspark
from pyspark.sql import SparkSession
from pyspark import SparkContext
from pyspark.streaming import StreamingContext

from riotwatcher import LolWatcher
import json
import random
import time
from math import log,inf

def createGameList(watcher,region):
    # used to call multiple games at once
    gamelist=[]
    for i in range (500):
        gamelist.extend(watcher.spectator.featured_games(region)["gameList"])
    return gamelist

def saveGameList(gamelist):
    with open('data', 'w') as f:
        for game in gamelist:
            f.write(json.dumps(game)+"\n")    
def getParticipantData(game):
    try:
        game=json.loads(game)
        participants=game["participants"]
        return [{'summonerName':participant['summonerName'],"championId":participant["championId"],"teamId":participant["teamId"],"gameId":game["gameId"] } for participant in participants if participant['bot']== False]
    except:
        pass
def getSummonerData(participants):
    from riotwatcher import LolWatcher
    watcher = LolWatcher(key)
    players=[]
    for player in participants:
        player_data=watcher.summoner.by_name(region,player["summonerName"])
        player["accountId"]=player_data["accountId"]
        player["summonerId"]=player_data["id"]
        players.append(player)
    return players
def getChampMastery(participants):
    from riotwatcher import LolWatcher
    watcher = LolWatcher(key)
    players=[]
    for player in participants:
        
        player_champ_data=watcher.champion_mastery.by_summoner_by_champion(region,player["summonerId"],player["championId"])
        
        stats={"championLevel":player_champ_data['championLevel'],
                "championPoints":player_champ_data['championPoints']}
        champ_familiarity=(int(round(time.time() * 1000)) - player_champ_data["lastPlayTime"])/1000 #converts it into seconds
        stats["champ_familiarity"]=champ_familiarity
        player["stats"]=stats
    
        players.append(player)
    return players
def getScore(participants):
    players=[]
    for player in participants:
        stats=player["stats"]
        score=log(stats["championLevel"]*stats["championPoints"])/log(stats["champ_familiarity"])
        player["score"]=score
        players.append(player)
    return players


def splitTeams(participants):
        blue=[]
        red=[]
        for player in participants:
            if player["teamId"]==100: blue.append(player)
            if player["teamId"]==200: red.append(player)
        return {"blue":blue,"red":red}
def getGamePrediction(participants):
    game_predictions={}
    for team_name in participants.keys():
        team=participants[team_name]
        total_score=0
        max={"score":-inf,"summonerName":""}
        for player in team:
            total_score+=player["score"]        
            if player["score"] >max["score"]:
                max["score"]=player["score"]
                max["summonerName"]=player["summonerName"]
        game_predictions[f"{team_name}TotalScore"]=total_score
        game_predictions[f"{team_name}ThreatName"]=max["summonerName"]
        game_predictions[f"{team_name}ThreatScore"]=max["score"]
        
    game_predictions[f"redThreatScore"]=game_predictions[f"redThreatScore"]/(game_predictions[f"redThreatScore"]+game_predictions[f"blueThreatScore"])
    game_predictions[f"blueThreatScore"]=game_predictions[f"blueThreatScore"]/(game_predictions[f"redThreatScore"]+game_predictions[f"blueThreatScore"])
    
    total_score=game_predictions["blueTotalScore"]+game_predictions[f"redTotalScore"]
    game_predictions["redWinProbability"]=100*game_predictions[f"redTotalScore"]/total_score
    game_predictions["blueWinProbability"]=100*game_predictions[f"blueTotalScore"]/total_score
    
    return game_predictions
        
        
if __name__ == "__main__":
        
        findspark.init()
        spark = SparkSession.builder.master("local[*]").getOrCreate()
        sc=spark.sparkContext
        ssc = StreamingContext(sc, 1)
        key='RGAPI-bf9365f8-34d6-45d1-b2dc-ca530963d7ca'
        watcher = LolWatcher(key)
        region = 'EUN1'
        
        games = ssc.socketTextStream("localhost", 9999)
        predictions=games.map(getParticipantData)\
            .map(getSummonerData)\
            .map(getChampMastery)\
            .map(getScore)\
            .map(splitTeams)\
            .map(getGamePrediction)
        # score=participants_per_game.map(getScore)
        # predictions.pprint()
        3
        ssc.start()
        ssc.awaitTermination()
    