import numpy as np
from colorama import Fore, Back, Style
#WWWWWWWWWGGGGGGGGGRRRRRRRRRBBBBBBBBBOOOOOOOOOYYYYYYYYY

class Cube:
    def __init__(self, str):
        self.faces = np.empty((6, 3, 3), dtype='<U1')
        for i in range(6):
            for j in range(3):
                for k in range(3):
                    self.faces[i][j][k] = str[i*9 + j*3 + k]
    
    
    def __str__(self) -> str:
        f = self.faces
        s = ""

        # U 
        for r in range(3):
            s += "       " + f[0][r][0] + " " + f[0][r][1] + " " + f[0][r][2] + "\n"

        # L F R B 
        for r in range(3):
            s += (
                f[1][r][0] + " " + f[1][r][1] + " " + f[1][r][2] + " " +
                " " +
                f[2][r][0] + " " + f[2][r][1] + " " + f[2][r][2] + " " +
                " " +
                f[3][r][0] + " " + f[3][r][1] + " " + f[3][r][2] + " " +
                " " +
                f[4][r][0] + " " + f[4][r][1] + " " + f[4][r][2] + " " +
                "\n"
            )

        # D 
        for r in range(3):
            s += "       " + f[5][r][0] + " " + f[5][r][1] + " " + f[5][r][2] + "\n"

        return s

    def pprint(self) -> None:
        color_map = {
            "R": Fore.RED,
            "G": Fore.GREEN,
            "B": Fore.BLUE,
            "O": "\033[38;2;255;140;0m",
            "W": Fore.WHITE,
            "Y": Fore.YELLOW,
        }
        for c in self.__str__():
            print(color_map.get(c, Fore.RESET) + c, end="")
        print(Style.RESET_ALL, end="")
        
    
    def turn(self, str):
        for move in str.split(" "):
            if move == "R":
                self.vertical_twist(2,1)
            elif move == "R'":
                self.vertical_twist(2,0)
            elif move == "L":
                self.vertical_twist(0,0)
            elif move == "L'":
                self.vertical_twist(0,1)
            elif move == "U":
                self.horizontal_twist(0,0)
            elif move == "U'":
                self.horizontal_twist(0,1)
            elif move == "D":
                self.horizontal_twist(2,1)
            elif move == "D'":
                self.horizontal_twist(2,0)
            elif move == "B":
                self.side_twist(2,1)
            elif move == "B'":
                self.side_twist(2,0)
            elif move == "F":
                self.side_twist(0,0)
            elif move == "F'":
                self.side_twist(0,1)
            else:
                print(f'ERROR - invalid move: {move}')
                return
        
        
    #direction: 0-left, 1-right
    #row: 0-top, 1-middle, 2-bottom
    def horizontal_twist(self, row, direction):
        if row < len(self.faces[0]):
            temp1 = self.faces[1][row].copy()
            temp2 = self.faces[2][row].copy()
            temp3 = self.faces[3][row].copy()
            temp4 = self.faces[4][row].copy()

            if direction == 0: #Twist left
                self.faces[1][row] = temp2
                self.faces[2][row] = temp3
                self.faces[3][row] = temp4
                self.faces[4][row] = temp1

            elif direction == 1: #Twist right
                self.faces[1][row] = temp4
                self.faces[2][row] = temp1
                self.faces[3][row] = temp2
                self.faces[4][row] = temp3

            else:
                print(f'ERROR - direction must be 0 (left) or 1 (right)')
                return

            #Rotating connected face
            if direction == 0: #Twist left
                if row == 0:
                    self.faces[0] = np.rot90(self.faces[0], -1) #Transpose top clockwise
                elif row == 2:
                    self.faces[5] = np.rot90(self.faces[5], 1) #Transpose bottom counter-clockwise

            elif direction == 1: #Twist right
                if row == 0:
                    self.faces[0] = np.rot90(self.faces[0], 1) #Transpose top counter-clockwise
                elif row == 2:
                    self.faces[5] = np.rot90(self.faces[5], -1) #Transpose bottom clockwise
        else:
            print(f'ERROR - desired row outside of rubiks cube range. Please select a row between 0-{len(self.faces[0])-1}')
            return

    #direction: 0-down, 1-up
    #column: 0-left, 1-middle, 2-right
    def vertical_twist(self, colum, direction):
        if colum < len(self.faces[0]):
            temp1 = self.faces[0][:,colum].copy()
            temp2 = self.faces[2][:,colum].copy()
            temp3 = self.faces[5][:,colum].copy()
            temp4 = self.faces[4][:,2-colum].copy()

            if direction == 0: #Twist down
                self.faces[0][:,colum] = np.flip(temp4)
                self.faces[2][:,colum] = temp1
                self.faces[5][:,colum] = temp2
                self.faces[4][:,2-colum] = np.flip(temp3)
            elif direction == 1: #Twist up
                self.faces[0][:,colum] = temp2
                self.faces[2][:,colum] = temp3
                self.faces[5][:,colum] = np.flip(temp4)
                self.faces[4][:,2-colum] = np.flip(temp1)
            else:
                print(f'ERROR - direction must be 0 (down) or 1 (up)')
                return

            #Rotating connected face
            if direction == 0: #Twist down
                if colum == 0:
                    self.faces[1] = np.rot90(self.faces[1], -1) #Transpose left clockwise
                elif colum == 2:
                    self.faces[3] = np.rot90(self.faces[3], 1) #Transpose right counter-clockwise
            
            elif direction == 1: #Twist up
                if colum == 0:
                    self.faces[1] = np.rot90(self.faces[1], 1) #Transpose left counter-clockwise
                elif colum == 2:
                    self.faces[3] = np.rot90(self.faces[3], -1) #Transpose right clockwise
        else:
            print(f'ERROR - desired column outside of rubiks cube range. Please select a column between 0-{len(self.faces[0])-1}')
            return
    
    #direction: 0-clockwise, 1-counter-clockwise
    #face: 0-front, 2-back    
    def side_twist(self, face, direction):
        if face < len(self.faces):
            if face == 0: #Front face
                temp1 = self.faces[0][2,:].copy()
                temp2 = self.faces[1][:,2].copy()
                temp3 = self.faces[3][:,0].copy()
                temp4 = self.faces[5][0,:].copy()

                if direction == 0: #Twist clockwise
                    self.faces[0][2,:] = np.flip(temp2)
                    self.faces[3][:,0] = temp1
                    self.faces[5][0,:] = np.flip(temp3)
                    self.faces[1][:,2] = temp4
                    self.faces[2] = np.rot90(self.faces[2], -1)
                elif direction == 1: #Twist counter-clockwise
                    self.faces[0][2,:] = temp3
                    self.faces[1][:,2] = np.flip(temp1)
                    self.faces[5][0,:] = temp2
                    self.faces[3][:,0] = np.flip(temp4)
                    self.faces[2] = np.rot90(self.faces[2], 1)
                else:
                    print(f'ERROR - direction must be 0 (clockwise) or 1 (counter-clockwise)')
                    return
            
            elif face == 2: #Back face
                temp1 = self.faces[0][0,:].copy()
                temp2 = self.faces[1][:,0].copy()
                temp3 = self.faces[3][:,2].copy()
                temp4 = self.faces[5][2,:].copy()
               

                if direction == 0: #Twist clockwise
                    self.faces[0][0,:] = np.flip(temp2)
                    self.faces[3][:,2] = temp1
                    self.faces[5][2,:] = np.flip(temp3)
                    self.faces[1][:,0] = temp4
                    self.faces[4] = np.rot90(self.faces[4], 1)
                elif direction == 1: #Twist counter-clockwise
                    self.faces[0][0,:] = temp3
                    self.faces[3][:,2] = np.flip(temp4)
                    self.faces[5][2,:] = temp2
                    self.faces[1][:,0] = np.flip(temp1)
                    self.faces[4] = np.rot90(self.faces[4], -1)
                else:
                    print(f'ERROR - direction must be 0 (clockwise) or 1 (counter-clockwise)')
                    return
