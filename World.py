from Component import Component
import random
import json

with open('Feature.json') as f:
  features = json.load(f)

class World:
    def __init__(self, mapSize = 20):
        self.mapSize = mapSize
        self.map = [["None" for _ in range(mapSize)] for _ in range(mapSize)]
        

        for i in range(self.mapSize):
            for j in range(self.mapSize):
                self.map[i][j] = Component((['@']+['.']*(self.mapSize**2-1))[i*self.mapSize+j],(i,j),self.mapSize,self)

    def map2String(self):
        result = ""
        for i in range(self.mapSize):
            result+=" ".join([str(j) for j in self.map[i]])+"\n"
        return result

    def statistic(self):
        text = ""
        for i in features:
            if i == " ": continue
            text+="\'{}\': {} ".format(i,self.map2String().count(i))
        seq = list()
        sumHealth = 0
        numberPredator = 0
        life = 0
        for i in self.map: seq+=i
        for i in seq: 
            if i.name != " ": life+=1
            if i.name == "@":
                numberPredator += 1
                sumHealth+=i.health
        if numberPredator != 0: text+=" avg health: "+str(sumHealth/numberPredator)
        return text,numberPredator,life

    def update(self):
        seq = list()
        for i in self.map: seq+=i
        random.shuffle(seq)
        for i in seq: i.alreadyMoved = False
        for i in seq:
            if i.name == " ": continue
            i.action()





          

                    
