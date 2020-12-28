import json
from riotwatcher import LolWatcher

def saveGameList(file_name,gamelist):
    with open(file_name, 'w') as f:
        for game in gamelist:
            f.write(json.dumps(game)+"\n")    

if __name__ == "__main__":
    key='RGAPI-bf9365f8-34d6-45d1-b2dc-ca530963d7ca'
    watcher = LolWatcher(key)
    region = 'EUN1'
    ground_truths=[]
    with open("./results/results3","r") as f:
         for line in f:
            data=json.loads(line)
            # print(data)
            result=watcher.match.by_id(region,data["gameId"])
            team=""
            if result["teams"][0]["win"]=="Win":
                if result["teams"][0]["teamId"]==100:
                    data["groundTruth"]="blue"
                else:
                    data["groundTruth"]="red"
            else:
                if result["teams"][0]["teamId"]==100:
                    data["groundTruth"]="red"
                else:
                    data["groundTruth"]="blue"
                
            ground_truths.append(data)
    saveGameList("ground_truth3.1",ground_truths)