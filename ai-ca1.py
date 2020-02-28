import copy
import numpy as np
def readFile(fileName) :
    file = open(fileName, 'r+')
    fList = file.readlines()
    file.close()
    fList = [s.replace('\n', '') for s in fList]
    return fList;

l1 = readFile("test1.txt")
l2 = readFile("test2.txt")
l3 = readFile("test3.txt")

class Node :
    def __init__(self, nodeType, capacity = 0) :
        self.visited = False
        self.type = nodeType #types -> b: block, a: ambulance, h: hospital, p: patient, s: space
        self.realType = nodeType
        self.capacity = capacity
        if (nodeType == 'a') :
            self.visited = True

class City :
    def __init__(self, table) :
        [self.ambX, self.ambY] = self.getAmbCoords(table);
        self.nodes = self.getTableNodes(table)
        self.stateChanged = False
        self.numsOfPatients = self.getNumOfPatients()
        self.bfsList = []
    def getAmbCoords(self, table) :
        for i in range(0, len(table)):
            for j in range(0, len (table[i])):
                if (table[i][j] == 'A') :
                    return [i, j]
        return [-1, -1]
    def getTableNodes(self, table) :
        nodes = []
        for i in range(0, len(table)):
            currentNodes = []
            for j in range(0, len (table[i])):
                if (table[i][j] == 'A'):
                    currentNodes.append(Node('a'))
                elif (table[i][j] == '#'):
                    currentNodes.append(Node('b'))
                elif (table[i][j] == 'P'):
                    currentNodes.append(Node('p'))
                elif (table[i][j] == ' '):
                    currentNodes.append(Node('s'))
                elif (table[i][j] == '0' or table[i][j] == '1' or table[i][j] == '2' or table[i][j] == '3'):
                    capacity = int(table[i][j])
                    currentNodes.append(Node('h', capacity))
                else :
                    currentNodes.append(Node('s'))
            nodes.append(currentNodes)
        return nodes
    def getNumOfPatients(self) :
        ans = 0
        for i in range(0, len(self.nodes)) :
            for j in range (0, len(self.nodes[i])):
                if self.nodes[i][j].type == 'p':
                    ans += 1
        return ans
    def printInfo(self):
        # print("ambulance: x =", self.ambX, " y =", self.ambY)
        # print("number of patients: ", self.numsOfPatients)
        print("table: ")
        for i in range(0, len(self.nodes)) :
            for j in range (0, len(self.nodes[i])):
                if self.nodes[i][j].type == 'b':
                    print('#', end = '')
                else :
                    print(self.nodes[i][j].type, end = '')
            print()
            
    def checkDirection(self, direction, s) :
        x = s[0]
        y = s[1]
        if (direction == 'u') :
            y += 1
        if (direction == 'r') :
            x += 1
        if (direction == 'd') :
            y -= 1
        if (direction == 'l') :
            x -= 1
        if (self.nodes[x][y].visited == True or self.nodes[x][y].type == 'b') :
            return False
        elif (self.nodes[x][y].type == 's' or self.nodes[x][y].type == 'h') :
            return True
        elif (self.nodes[x][y].type == 'p') : 
            if (direction == 'u') :
                y += 1
            if (direction == 'r') :
                x += 1
            if (direction == 'd') :
                y -= 1
            if (direction == 'l') :
                x -= 1
            if (self.nodes[x][y].type == 's' or self.nodes[x][y].type == 'h') :
                return True
            else :
                return False
    def clearVisiteds(self) : 
        for i in range(0, len(self.nodes)) :
            for j in range (0, len(self.nodes[i])):
                self.nodes[i][j].visited = False
    def BfsMove(self, s) : 
        x = s[0]
        y = s[1]
        newX = s[0]
        newY = s[1]
        direction = s[2]
        break2 = False
        for i in range(0, len(self.nodes)) :
            if break2 : 
                break
            for j in range (0, len(self.nodes[i])):
                if (self.nodes[i][j].type == 'a') : 
                    if (self.nodes[i][j].realType == 'h') : 
                        self.nodes[i][j].type = 'h'
                    else :
                        self.nodes[i][j].type = 's'
                    break2 = True
                    break
        if (self.nodes[x][y].type == 'p') :
            self.clearVisiteds() 
            if (direction == 'u') :
                newY += 1
            if (direction == 'r') :
                newX += 1
            if (direction == 'd') :
                newY -= 1
            if (direction == 'l') :
                newX -= 1
            if (self.nodes[newX][newY].type == 's') :
                self.nodes[newX][newY].type = 'p';
            elif (self.nodes[newX][newY].type == 'h' and self.nodes[newX][newY].capacity > 0) :
                self.nodes[newX][newY].capacity -= 1;
            elif (self.nodes[newX][newY].type == 'h' and self.nodes[newX][newY].capacity == 0) :
                self.nodes[newX][newY].type = 'p';
        self.nodes[x][y].visited = True
        self.nodes[x][y].type = 'a'
    def bfsSolution(self) :
        q = []
        start = True
        reachEnd = False
        while (reachEnd == False) :
            if (start) : 
                s = [self.ambX, self.ambY, 0]
                x = self.ambX
                y = self.ambY
                path = ''
                self.nodes[x][y].visited = True
                start = False
            else :
                s = q[0]
                x = s[0]
                y = s[1]
                path = s[4]
                q.pop(0)
                self.nodes[x][y].visited = True
                self.nodes = s[3]
                self.BfsMove([s[0], s[1], s[2]])
            # print("x :", x, "y :", y, "dis: ", s[2])
            print()
            print("path: ", len(path))
            # self.printInfo()
            # print("patients: ", self.getNumOfPatients())
            print()
            tempNodes = []
            np.copyto(tempNodes, self.nodes)
                    
            if (self.checkDirection('u', [x, y])) :
                q.append([s[0], s[1] + 1, 'u', tempNodes, path+'r'])
            if (self.checkDirection('r', [x, y])) :
                q.append([s[0] + 1, s[1], 'r', tempNodes, path+'d'])
            if (self.checkDirection('d', [x, y])) :
                q.append([s[0], s[1] - 1, 'd', tempNodes, path+'l'])
            if (self.checkDirection('l', [x, y])) :
                q.append([s[0] - 1, s[1], 'l', tempNodes, path+'u'])
            if (self.getNumOfPatients() == 0 or len(q) == 0) : 
                reachEnd = True
                

        
city1 = City(l1)
city2 = City(l2)
city3 = City(l3)

# city1.printInfo()
# city2.printInfo()
# city3.printInfo()
city3.bfsSolution()