import copy
import time
def readFile(fileName) :
    file = open(fileName, 'r+')
    fList = file.readlines()
    file.close()
    fList = [s.replace('\n', '') for s in fList]
    return fList;

l1 = readFile("test1.txt")
l2 = readFile("test2.txt")
l3 = readFile("test3.txt")
def sortSecond(val): 
    return val[1]
class Node :
    def __init__(self, nodeType) :
        self.type = nodeType #types -> b: block, s: space

class Obj:
    def __init__(self, x, y, nodeType, capacity = 0) : 
        self.x = x
        self.y = y
        self.type = nodeType
        self.realType = nodeType
        self.capacity = capacity

class City :
    def __init__(self, table) :
        self.table = self.getTableNodes(table)
        self.bfsList = []
        self.currentState = self.getInitialState(table) #[0] state of a, p , and h.     [1] hash.       [2] path
        self.currentStateCopy = copy.deepcopy(self.currentState)
        self.q = []
    def getTableNodes(self, table) :
        nodes = []
        for i in range(0, len(table)):
            currentNodes = []
            for j in range(0, len (table[i])): 
                if (table[i][j] == '#'):
                    currentNodes.append(Node('b'))
                else :
                    currentNodes.append(Node('s'))
            nodes.append(currentNodes)
        return nodes
      
    def getHash(self, objList): 
        currentHash = '' 
        currentP = []
        currentH = []
        currentA = []
        currentType = 'p'
        
        for i in objList: 
            if (i.type == 'p') :
                currentP.append([i.x, i.y])
            if (i.type == 'h') :
                currentH.append([i.x, i.y])
            if (i.type == 'a') :
                currentA.append([i.x, i.y]) 
        currentP.sort(key = sortSecond)
        currentH.sort(key = sortSecond)
        currentA.sort(key = sortSecond) 
        currentP.sort()
        currentH.sort()
        currentA.sort()  
        for i in currentP:
            currentHash += str(i[0]) + "|" + str(i[1]) + "|" + 'p' + "|" 
        currentHash += "#"
        for i in currentH:
            currentHash += str(i[0]) + "|" + str(i[1]) + "|" + 'h' + "|" 
        currentHash += "#"
        for i in currentA:
            currentHash += str(i[0]) + "|" + str(i[1]) + "|" + 'a' + "|"
        return currentHash
    def getInitialState(self, table) : 
        currentState = []
        currentState0 = []
        for i in range(0, len(table)):
            for j in range(0, len (table[i])): 
                if (table[i][j] == 'P'):
                    currentState0.append(Obj(i, j, 'p'))
                elif (table[i][j] == '0' or table[i][j] == '1' or table[i][j] == '2' or table[i][j] == '3') : 
                    capacity = int(table[i][j])
                    currentState0.append(Obj(i, j, 'h', capacity))
                elif (table[i][j] == 'A') : 
                    currentState0.append(Obj(i, j, 'a'))
        currentHash = self.getHash(currentState0)
        currentPath = '' 
        currentState.append(currentState0)
        currentState.append(currentHash)
        currentState.append(currentPath)
        print("currentHash: ", currentHash)        
        return currentState
    def getNumOfPatients(self) :
        ans = 0
        for i in range(0, len(self.currentState[0])) :
            if self.currentState[0][i].type == 'p':
                ans += 1
        return ans
    
    def currentAmbulanceCoord(self) : 
        for i in self.currentState[0] :
            if i.type == 'a':
                return [i.x, i.y]
        return [-1, -1]
    def getNewDir(self, direction) : 
        if (direction == 'u') :
            return 'r'
        if (direction == 'r') :
            return 'd'
        if (direction == 'd') :
            return 'l'
        if (direction == 'l') :
            return 'u'
    def getNewXY(self, x, y, direction) : 
        if (direction == 'u') : 
            return [x, y + 1]
        if (direction == 'r') : 
            return [x + 1, y]
        if (direction == 'd') : 
            return [x, y - 1]
        if (direction == 'l') : 
            return [x - 1, y]
    
    def getCurrentObj(self, x, y) :
        if (self.table[x][y].type == 'b') : 
            return 'b'
        for i in self.currentState[0] : 
            if (i.x == x and i.y == y) : 
                return i
        return 's'
    def setNewAmbulance(self, x, y, newX, newY) :
        for i in range(0, len(self.currentState[0])) : 
            if (self.currentState[0][i].x == x and self.currentState[0][i].y == y and self.currentState[0][i].type == 'a' and self.currentState[0][i].realType != 'h') :
                self.currentState[0].pop(i)
                break
            elif (self.currentState[0][i].x == x and self.currentState[0][i].y == y and self.currentState[0][i].type == 'a' and self.currentState[0][i].realType == 'h') :
                self.currentState[0][i].type = 'h'
                break
        tempObj = self.getCurrentObj(newX, newY)
        if (tempObj == 's') :
            newObj = Obj(newX, newY, 'a')
            self.currentState[0].append(newObj)
        elif (tempObj != 'b' and ((tempObj.type == 'h') or (tempObj.type == 'p'))) : 
            for i in range(0, len(self.currentState[0])) : 
                if (self.currentState[0][i].x == newX and self.currentState[0][i].y == newY) :
                    self.currentState[0][i].type = 'a'
                    break
                
    def setNewPatient(self, newX, newY) : 
        for i in range(0, len(self.currentState[0])) : 
            if (self.currentState[0][i].x == newX and self.currentState[0][i].y == newY and self.currentState[0][i].type == 'h' and self.currentState[0][i].capacity > 0) :
                self.currentState[0][i].capacity -= 1
                return
            elif (self.currentState[0][i].x == newX and self.currentState[0][i].y == newY and self.currentState[0][i].type == 'h' and self.currentState[0][i].capacity <= 0) :
                self.currentState[0][i].type = 'p'
                return
        newObj = Obj(newX, newY, 'p')
        self.currentState[0].append(newObj)
        return
                
    def checkDirectionAndState(self, x, y, direction):
        [newX,newY] = self.getNewXY(x, y, direction)
        # print("aaaa : ", newX, newY)
        if (self.table[newX][newY].type == 'b') : 
            # print("here1")
            return -1
        currentObj = self.getCurrentObj(newX, newY)
        if (currentObj == 's' or currentObj.type == 'h') :
            self.setNewAmbulance(x, y, newX, newY)
        elif (currentObj.type == 'p') :
            [newNewX, newNewY] = self.getNewXY(newX, newY, direction)
            if (self.table[newNewX][newNewY].type == 'b') : 
                # print("here2")
                return -1
            currentObj = self.getCurrentObj(newNewX, newNewY)
            if (currentObj != 's' and currentObj.type == 'p') :
                # print("here3")
                return -1
            self.setNewAmbulance(x, y, newX, newY)
            self.setNewPatient(newNewX, newNewY)
        self.currentState[1] = self.getHash(self.currentState[0])
        self.currentState[2] = self.currentState[2] + self.getNewDir(direction)
        # print("here here : ", self.currentState[1])
        return 1
        
    def isRepetitiveState(self) : 
        cnt = 0
        for i in self.q :
            cnt += 1
            if i[1] == self.currentState[1] : 
                return True
        return False
    def getCopy(self) : 
        currentState = []
        currentState0 = []
        for i in range(0, len(table)):
            for j in range(0, len (table[i])): 
                if (table[i][j] == 'P'):
                    currentState0.append(Obj(i, j, 'p'))
                elif (table[i][j] == '0' or table[i][j] == '1' or table[i][j] == '2' or table[i][j] == '3') : 
                    capacity = int(table[i][j])
                    currentState0.append(Obj(i, j, 'h', capacity))
                elif (table[i][j] == 'A') : 
                    currentState0.append(Obj(i, j, 'a'))
    def bfsSolution(self) :
        start = True
        counter = 0
        reachEnd = False
        while (reachEnd == False) :
            counter += 1
            if (start) : 
                start = False
            else :
                self.currentState = self.q[0]
                self.currentStateCopy = self.getCopy()
                self.q.pop(0)
            print("hash : " ,self.currentState[1])
            print("path : " ,self.currentState[2])
            print("len : ", len(self.currentState[2]))
            print()
            [x, y] = self.currentAmbulanceCoord()
            
            
            uResult = self.checkDirectionAndState(x, y, 'u')
            if (uResult == 1 and self.isRepetitiveState() == False) : 
                self.q.append(self.currentState)
            self.currentState = copy.deepcopy(self.currentStateCopy)
            
            rResult = self.checkDirectionAndState(x, y, 'r')
            if (rResult == 1 and self.isRepetitiveState() == False) : 
                self.q.append(self.currentState)
            self.currentState = copy.deepcopy(self.currentStateCopy)
            
            dResult = self.checkDirectionAndState(x, y, 'd')
            if (dResult == 1 and self.isRepetitiveState() == False) : 
                self.q.append(self.currentState)
            self.currentState = copy.deepcopy(self.currentStateCopy)
                
            lResult = self.checkDirectionAndState(x, y, 'l')
            if (lResult == 1 and self.isRepetitiveState() == False) : 
                self.q.append(self.currentState)
            self.currentState = copy.deepcopy(self.currentStateCopy)
            
            print("len(q): ", len(self.q))
            print()
            if (self.getNumOfPatients() == 0 or len(self.q) == 0) : 
                print("len(q): ", len(self.q))
                reachEnd = True
                

        
city1 = City(l1)
city2 = City(l2)
city3 = City(l3)

start = time.time()
city2.bfsSolution()

end = time.time()
print(end - start)
