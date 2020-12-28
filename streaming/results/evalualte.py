import json
def saveGameList(file_name,gamelist):
    with open(file_name, 'w') as f:
        for game in gamelist:
            f.write(json.dumps(game)+"\n")    

if __name__ == "__main__":
    ground_truths=[]
    with open("./results/ground_truth1.1","r") as f:
        blue_counter=0
        red_counter=0
        total=0
        for line in f:
            data=json.loads(line)
            if data["blueWinProbability"] >50 and data["groundTruth"] =="blue":
                blue_counter+=1
            if data["redWinProbability"] >50 and data["groundTruth"] =="red":
                red_counter+=1
            total+=1
        print(100*blue_counter/total)
        print(100*red_counter/total)
            # print(data)
            
            