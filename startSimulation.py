from World import World
import time


if __name__ == "__main__":
    world = World() 
    _,nPredator,life = world.statistic()
    maxPredator = nPredator
    i = 0
    while life != 0 and nPredator !=0:
        
        i+=1
        time.sleep(0.1)
        world.update()
        print(chr(27) + "[2J")
        print(world.map2String(),end='')
        stats, nPredator,life = world.statistic()
        if nPredator > maxPredator: maxPredator = nPredator
        print(i,stats,'max:',maxPredator,"life:",life)



    