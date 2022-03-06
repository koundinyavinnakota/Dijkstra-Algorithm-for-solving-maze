import numpy as np
import cv2

class Map:

    def __init__(self,clearance=2):
        self.image =  np.zeros((250,400,3),dtype="uint8")
        # self.image = cv2.cvtColor(self.image, cv2.CV_8U)
        self.clearance=clearance
        self.obstacleSpace()

    def obstacleSpace(self):
        for x in range(400):
            for y in range (250):
                # Defining a circle
                circle = (y-65) * (y-65) + (x-300) * (x-300) - (40 + self.clearance) ** 2

                # The four sided polygon has been divided into two triangles for defining the half planes
                # The three lines of the first triangle
                poly_1 = y + (0.37)*x + (-76.4 + self.clearance)
                poly_2 = y + (-0.114)*x + (-60.91)
                poly_3 = y + (0.86)*x + (-138.6 - self.clearance)

                # The three lines of the second triangle
                poly_4 = y + (-1.232)*x + (-20.65 - self.clearance)
                poly_5 = y + (-0.114)*x + (-60.91)
                poly_6 = y + (-3.2)*x + (186 + self.clearance)

                # Hexagon
                hex_1= y + (0.57)*x + (-224.29 + self.clearance)
                hex_2= y + (-0.57)*x + (4.29 +self.clearance)
                hex_3= x + (-235 - self.clearance)
                hex_4= y + (0.57)*x + (-304.29 -self.clearance)
                hex_5= y + (-0.57)*x + (-75.71 - self.clearance)
                hex_6= x + (-165 + self.clearance)

                # Condition for circle, Polygon & Hexagon
                if circle < 0 or (poly_1 > 0 and poly_2 < 0 and poly_3 < 0) or (poly_4 <0 and poly_5>0 and poly_6 > 0) or (hex_1 >0 and hex_2 >0 and hex_3 <0 and hex_4 <0 and hex_5 <0 and hex_6 >0):
                    self.image[y,x,2] = 255
                else :

                    self.image[y,x] = 0

# Class
class node(Map):

    def __init__(self,row,col):
        super().__init__()
        self.row=row
        self.col=col
        self.costToCome=0
        self.costMap={"u":1,"ul":1.4,"ur":1.4, "r":1,"d":1,"dl":1.4,"dr":1.4,"l":1 }
        self.parent=()
        self.listofChildNodes={}


    #Checks nodes in Obstacle Space
    def checkObstacleSpace(self,row,col):
        if np.array_equal(self.image[row,col],[0,0,255]):
            print("Within the obstacle space")
            return True
        else :
            return False

#This function checks for all the child nodes
    def possibleMovements(self):
        #This conditon checks for possibility in the "UP" direction
        if self.row < 250 and self.row > 0 and self.col >= 0 and self.col < 400:
            if not self.checkObstacleSpace(self.row - 1,self.col):

                self.listofChildNodes[(self.row - 1,self.col)]=self.costToCome + self.costMap["u"]


        #This condition checks for possibility in "UP-LEFT" direction
        if self.col > 0 and self.col  < 400 and self.row < 250 and self.row > 0:
            if not self.checkObstacleSpace(self.row - 1,self.col - 1):
                self.listofChildNodes[(self.row - 1,self.col - 1)]=self.costToCome + self.costMap["ul"]


        #This condition checks for possibility in "UP_RIGHT" direction.
        if self.row < 250 and self.row > 0 and self.col >= 0 and self.col < 399:
            if not self.checkObstacleSpace(self.row - 1,self.col + 1):
                self.listofChildNodes[(self.row - 1,self.col + 1)]=self.costToCome + self.costMap["ur"]


        #This condition checks for possibility in "RIGHT" direction.
        if self.row < 250 and self.row >= 0 and self.col >= 0 and self.col < 399:

            if not self.checkObstacleSpace(self.row,self.col + 1):
                self.listofChildNodes[(self.row,self.col + 1)]=self.costToCome + self.costMap["r"]


        #This condition checks for possibility in "DOWN" direction.
        if self.row < 249 and self.row >= 0 and self.col >= 0 and self.col < 400:
            if not self.checkObstacleSpace(self.row + 1,self.col):
                self.listofChildNodes[(self.row + 1,self.col)]=self.costToCome + self.costMap["d"]


        #This condition checks for possibility in "DOWN-LEFT" direction.
        if self.row < 249 and self.row >= 0 and self.col > 0 and self.col < 400:
            if not self.checkObstacleSpace(self.row + 1,self.col-1):

                self.listofChildNodes[(self.row + 1,self.col - 1)]=self.costToCome + self.costMap["dl"]


        #This condition checks for possibility in "DOWN-RIGHT" direction.
        if self.row < 249 and self.row >= 0 and self.col >= 0 and self.col < 400:
            if not self.checkObstacleSpace(self.row + 1,self.col + 1):
                self.listofChildNodes[(self.row + 1,self.col + 1)]=self.costToCome + self.costMap["dr"]


        #This condition checks for possibility in "LEFT" direction.
        if self.row < 250 and self.row >= 0 and self.col > 0 and self.col < 400:
            if not self.checkObstacleSpace(self.row,self.col - 1):
                self.listofChildNodes[(self.row,self.col - 1)]=self.costToCome + self.costMap["l"]




def algo(start_node,goal_node):
    openList=[]
    closedlist=[]
    goalFlag=False
    openFlag=False
    closedFlag=False
    index=0

    n=node(start_node[0],start_node[1])
    n.parent=1
    openList.append(n)
    while openList and  not goalFlag:
        openFlag=False
        closedFlag=False
        leastCost=openList[0].costToCome
        index=0
        for a in openList:
            if a.costToCome < leastCost:
                index=openList.index(a)
                leastCost=a.costToCome

        openList[index].possibleMovements()

        for i in openList[index].listofChildNodes:
            closedFlag=False
            openFlag=False

            for a in openList:
                if a.row == i[0] and a.col == i[1]:
                    openFlag = True
                    if a.costToCome > (openList[index].costToCome + openList[index].listofChildNodes[i]):
                        a.costToCome = openList[index].costToCome + openList[index].listofChildNodes[i]
                    break

            for b in closedlist:
                if b.row == i[0] and b.col == i[1]:
                    closedFlag = True
                    break

            if not (openFlag) and not (closedFlag):
                n=node(i[0],i[1])
                print(" New Node :",i[0]," ",i[1])
                n.parent=(openList[index].row,openList[index].col)
                n.costToCome =  openList[index].listofChildNodes[i]
                openList.append(n)

        throw = openList.pop(index)
        if throw.row == goal_node[0] and throw.col ==goal_node[1]:
            goalFlag=True
            print("Horray !!!Goal is Reached ","costToCome goal",throw.costToCome)

        closedlist.append(throw)

    map=Map(0)
    fps=520
    w,h,_ = map.image.shape
    optimalPath=backtracking(closedlist,goal_node)
    print(optimalPath)
    writer = cv2.VideoWriter('maze_solver.avi', cv2.VideoWriter_fourcc(*'XVID'), fps, (h,w))

    for a in closedlist:
        map.image[a.row,a.col]=[255,0,0]
        writer.write(map.image)
        cv2.imshow("MazeSolver",map.image)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    for b in optimalPath:
        map.image[b[0],b[1]]=[0,255,0]
        writer.write(map.image)
        cv2.imshow("Result",map.image)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    writer.release()
    cv2.destroyAllWindows()

def backtracking(closedlist, goal_node):
    closedlist.reverse()
    element=closedlist[0].parent
    optimalPath=[]
    optimalPath.append((closedlist[0].row,closedlist[0].col))
    flag=True
    while flag:
        for a in closedlist:
            if element == (a.row,a.col):
                optimalPath.append((a.row,a.col))
                element = a.parent
            if optimalPath[-1] == (goal_node[0],goal_node[1]):
                flag= False
    return optimalPath

if __name__ == "__main__":
    x1,y1 = input("Enter start node with a space in between two digits: ").split()
    x1 = int(x1)
    y1= int(y1)
    x2,y2=input("Enter goal node with a space in between two digits :").split()
    x2=int(x2)
    y2=int(y2)
    algo((x1,y1),(x2,y2))
