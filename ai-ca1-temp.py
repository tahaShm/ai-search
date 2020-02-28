import copy
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
            
    def checkPossiblity(self, x, y, direction):
        if (self.nodes[x][y].visited == True) :
            return False
        if (self.nodes[x][y].type == 's' or self.nodes[x][y].type == 'h') :
            return True
        elif (self.nodes[x][y].type == 'b') :
            return False
        elif (self.nodes[x][y].type == 'p') :
            if (direction == 'u'):
                y += 1
            if (direction == 'r'):
                x += 1
            if (direction == 'd'):
                y -= 1
            if (direction == 'l'):
                x -= 1
            if (self.nodes[x][y].type == 's' or self.nodes[x][y].type == 'h') :
                return True
            else :
                return False
    def checkDirection(self, direction):
        possibility = False
        x = self.ambX
        y = self.ambY
        if (direction == 'u') :
            y += 1
        if (direction == 'r') :
            x += 1
        if (direction == 'd') :
            y -= 1
        if (direction == 'l') :
            x -= 1
        possibility = self.checkPossiblity(x, y, direction)
        return possibility
    def moveInBfs(self):
        x = self.bfsList[0][0]
        y = self.bfsList[0][1]
        x1 = x
        y1 = y
        x2 = x
        y2 = y        
        direction = self.bfsList[0][2]
        self.nodes[x][y].visited = True
        if (direction == 'u') :
            y1 -= 1
        if (direction == 'r') :
            x1 -= 1
        if (direction == 'd') :
            y1 += 1
        if (direction == 'l') :
            x1 += 1
            
        self.nodes[x1][y1].type = 's' #change previous position of ambulance to space type
    
        if (self.nodes[x2][y2].type == 'p') :
            self.stateChanged = True
            if (direction == 'u') :
                y2 += 1
            if (direction == 'r') :
                x2 += 1
            if (direction == 'd') :
                y2 -= 1
            if (direction == 'l') :
                x2 -= 1
            if self.nodes[x2][y2].type == 's' : 
                self.nodes[x2][y2].type == 'p'
            elif self.nodes[x2][y2].type == 'h' and self.nodes[x2][y2].capacity > 0 : 
                
                self.nodes[x2][y2].capacity -= 1
                if (self.nodes[x2][y2].capacity == 0) : 
                    self.nodes[x2][y2].type = 's'
        self.nodes[x][y].type = 'a'
        self.ambX = x
        self.ambY = y 
               
        print()
        print("direction: ", direction)
        self.printInfo()
        print()
        # print()
    def bfsSolution(self) :
        tempNodes = copy.deepcopy(self.nodes)
        print("current : ", self.ambX, self.ambY)
        if (self.checkDirection('u')) :
            # print("u : ", self.ambX, self.ambY + 1)
            self.bfsList.append([self.ambX, self.ambY + 1, 'u', tempNodes])
        if (self.checkDirection('r')) :
            # print("r : ", self.ambX + 1, self.ambY)
            self.bfsList.append([self.ambX + 1, self.ambY, 'r', tempNodes])
        if (self.checkDirection('d')) :
            # print("d : ", self.ambX, self.ambY - 1)
            self.bfsList.append([self.ambX, self.ambY - 1, 'd', tempNodes])
        if (self.checkDirection('l')) :
            # print("l : ", self.ambX - 1, self.ambY)
            self.bfsList.append([self.ambX - 1, self.ambY, 'l', tempNodes])
        # print("list size: ", len(self.bfsList))
        if len(self.bfsList) == 0 : 
            return 0  
        self.moveInBfs()
        self.nodes = self.bfsList[0][3] 
        self.bfsList.pop(0)
        if (self.numsOfPatients == 0 or len(self.bfsList) == 0) :
            return 1
        return self.bfsSolution()

        
city1 = City(l1)
city2 = City(l2)
city3 = City(l3)

# city1.printInfo()
# city2.printInfo()
# city3.printInfo()
print(city1.bfsSolution())
















import copy
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
        if (self.nodes[x][y].visited == True or self.nodes[x][y].type == 'b' or self.nodes[x][y].type == 'p') :
            return False
        elif (self.nodes[x][y].type == 's' or self.nodes[x][y].type == 'h') :
            return True
            
    def bfsSolution(self) :
        q = []
        q.append([self.ambX, self.ambY, 0])
        print("hhh")
        reachEnd = False
        while (reachEnd == False) :
            s = q[0]
            x = s[0]
            y = s[1]
            q.pop(0)
            self.nodes[x][y].visited = True
            print("x :", x, "y :", y, "dis: ", s[2])
            if (self.checkDirection('u', s)) :
                q.append([s[0], s[1] + 1, s[2]+1])
            if (self.checkDirection('r', s)) :
                q.append([s[0] + 1, s[1], s[2]+1])
            if (self.checkDirection('d', s)) :
                q.append([s[0], s[1] - 1, s[2]+1])
            if (self.checkDirection('l', s)) :
                q.append([s[0] - 1, s[1], s[2]+1])
            if (numsOfPatients == 0) : 
                reachEnd = True
                

        
city1 = City(l1)
city2 = City(l2)
city3 = City(l3)

# city1.printInfo()
# city2.printInfo()
# city3.printInfo()
city1.bfsSolution()