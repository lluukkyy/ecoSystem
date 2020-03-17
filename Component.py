import random
import json

with open('Feature.json') as f:
  features = json.load(f)

class Component:
    def __init__(self,name,location,mapSize,world,health=None):
        self.name = name
        if self.name!= " ":
            if not health: self.health = features[name]["health"]["maxHealth"]
            else: self.health = health
      
        self.alreadyMoved = False
        self.location = location
        self.mapSize = mapSize
        self.world = world

       
    def action(self):
        if self.name == " ": return
        actions = []
        for i in ["move","duplicate","eat"]:
            if random.random()>=0.05: actions.append(i)
        random.shuffle(actions)
        for a in actions:
            eval("self.{}()".format(a))
        self.health+= features[self.name]["health"]["dailyChange"]
        if self.health<=0:
            self.world.map[self.location[0]][self.location[1]] = Component(' ',self.location,self.mapSize,self.world)

    def probe(self,p):
        result = 0
        for i,j in [(-1,-1),(-1,0),(-1,1),(0,-1),(0,0),(0,1),(1,-1),(1,0),(1,1)]:
            newX,newY =p[0]+i,p[1]+j
            if newX>=0 and newX < self.mapSize and newY>=0 and newY < self.mapSize and (newX,newY)!=self.location:
                result+=features[self.name]["moveIntent"][self.world.map[newX][newY].name]
        return result

    def moveIntent(self):
        intent = -99999
        x,y = 0,0
        intentList = []
        for i,j in [(-1,-1),(-1,0),(-1,1),(0,-1),(0,0),(0,1),(1,-1),(1,0),(1,1)]:
            newX,newY = self.location[0]+i,self.location[1]+j
            if newX>=0 and newX < self.mapSize and newY>=0 and newY < self.mapSize:
                temp = self.probe((newX,newY))
                intentList.append((temp,(i,j)))
                if temp>intent:
                    intent = temp
                    x,y = i,j
        possibleMoves = []
        for i in intentList:
            if i[0] == intent:
                possibleMoves.append(i[1])
        return random.choice(possibleMoves)

    def move(self):
        if self.alreadyMoved: return
        x,y = self.location
        mi = self.moveIntent()
        newX, newY = x+mi[0], y+mi[1]
        newX = min(self.mapSize-1,max(newX,0))
        newY = min(self.mapSize-1,max(newY,0))

        if (newX,newY) == self.location: return
        
        temp = self.world.map[newX][newY]
        if temp.alreadyMoved:
            return
       
        temp.alreadyMoved = True
        temp.location = (x,y)

        self.alreadyMoved = True
        self.location = (newX,newY)
        
        self.world.map[newX][newY] = self
        self.world.map[x][y] = temp


    def eat(self):
        if self.name != "@": return
        for i,j in [(-1,-1),(-1,0),(-1,1),(0,-1),(0,0),(0,1),(1,-1),(1,0),(1,1)]:
            newX,newY = self.location[0]+i,self.location[1]+j
            if newX>=0 and newX < self.mapSize and newY>=0 and newY < self.mapSize and self.world.map[newX][newY].name=='.':
                temp =  self.world.map[newX][newY]
                temp.name  = " "
                temp.health = features[temp.name]["health"]["maxHealth"]
                self.health += 1
                break
        
        
        
    def duplicate(self):
        if random.random() >= features[self.name]["duplicate"]["rate"]: return
        if self.health<features[self.name]["duplicate"]["minHealth"]: return
        for _ in range(features[self.name]["duplicate"]["number"]):
            for i,j in [(-1,-1),(-1,0),(-1,1),(0,-1),(0,0),(0,1),(1,-1),(1,0),(1,1)]:
                newX,newY = self.location[0]+i,self.location[1]+j
                if newX>=0 and newX < self.mapSize and newY>=0 and newY < self.mapSize and self.world.map[newX][newY].name==' ':
                    child = Component(self.name,(newX,newY),self.mapSize,self.world,health=self.health*features[self.name]["duplicate"]["childHealthPercentage"])
                    child.mutate()
                    self.world.map[newX][newY] = child
                    self.health *= (1-features[self.name]["duplicate"]["childHealthPercentage"])
                    break
    

       
    def mutate(self):
        randomFloat = random.random()
        for o in features[self.name]['mutateOptions']:
            x,y = features[self.name]['mutateOptions'][o]
            if x<=randomFloat and randomFloat<y: 
                self.name = o
                break    

    def __minDir2(self,p):
        x,y = 0,0
        d = 9999
        for i,j in [(-1,-1),(-1,0),(-1,1),(0,-1),(0,0),(0,1),(1,-1),(1,0),(1,1)]:
            temp = (p[0]-self.location[0]-i)**2+(p[1]-self.location[1]-j)**2 
            if temp< d: 
                d = temp
                x,y = i,j
        return (x,y)

    def __str__(self):
        return str(self.name)