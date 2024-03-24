import tkinter as tk
from PIL import ImageTk, Image  

BOARD_HEIGHT = 20
BOARD_WIDTH  = 20

EMPTY = 0
PLAYER = 1
PINKY = 5
ROCKY = 6
POGO = 7
RINGO = 8
POWERUP = 4
CHERRY = 3
WALL = 2
UP = 3
DOWN = 1
LEFT = 2
RIGHT = 0

class GUI:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Pacman")
        self.frame = tk.Frame(self.window)
        self.frame.pack()
        self.canvas = tk.Canvas(self.frame, width=410, height=430, background="gray")
        self.canvas.pack()

        self.pacman0Img = Image.open("./Images/Pacman0.png")
        self.pacman1Img = Image.open("./Images/Pacman1.png")
        self.pacman2Img = Image.open("./Images/Pacman2.png")
        self.pacman3Img = Image.open("./Images/Pacman3.png")
        self.pacman4Img = Image.open("./Images/Pacman4.png")
        self.ghost1Img = Image.open("./Images/Pinky.png")
        self.ghost2Img = Image.open("./Images/Rocky.png")
        self.ghost3Img = Image.open("./Images/Pogo.png")
        self.ghost4Img = Image.open("./Images/Ringo.png")
        self.ghost5Img = Image.open("./Images/Vulnerable.png")
        self.ghost6Img = Image.open("./Images/Flash.png")
        self.cherryImg = Image.open("./Images/Cherry.png")

        self.arrowsImg = Image.open("./Images/arrowKeys.png")
        self.snacksMem = [[] for row in range(BOARD_HEIGHT)]
        for i,row in enumerate(self.snacksMem):
            self.snacksMem[i] = [0 for cell in range(BOARD_WIDTH)]
        self.cherryMem = (0,0)
        self.powerUpMem = []
    
    def roundPosition(self, position):
        while position >= BOARD_HEIGHT:
            position -= BOARD_HEIGHT
        while position < 0:
            position += BOARD_HEIGHT
        return position

    def smoothMove(self, entity, moveOffset, direction, moved):
        checkDir = (0,1)
        if direction == DOWN:
            checkDir = (0,-1)
        if direction == LEFT:
            checkDir = (-1,0)
        if direction == RIGHT:
            checkDir = (1,0)
        
        checkDir = (self.roundPosition(checkDir[0]+entity[0]), self.roundPosition(checkDir[1]+entity[1]))
        if not moved:
            return entity
        
        if direction == UP:
            return (entity[0],entity[1]+moveOffset/5-1)
        if direction == DOWN:
            return (entity[0],entity[1]-moveOffset/5+1)
        if direction == LEFT:
            return (entity[0]-moveOffset/5+1,entity[1])
        if direction == RIGHT:
            return (entity[0]+moveOffset/5-1,entity[1])

    def update(self, board, snacks, powerUps, direction, moveOffset, moved, ghosts, player, powerUpCount, score):
        offset = 5
        cellSize = 20

        pacman = [ImageTk.PhotoImage(self.pacman0Img.rotate(direction[0]*90)),
                  ImageTk.PhotoImage(self.pacman1Img.rotate(direction[0]*90)),
                  ImageTk.PhotoImage(self.pacman2Img.rotate(direction[0]*90)),
                  ImageTk.PhotoImage(self.pacman3Img.rotate(direction[0]*90)),
                  ImageTk.PhotoImage(self.pacman4Img.rotate(direction[0]*90))]
        ghostImges = [ImageTk.PhotoImage(self.ghost1Img), 
                      ImageTk.PhotoImage(self.ghost2Img), 
                      ImageTk.PhotoImage(self.ghost3Img), 
                      ImageTk.PhotoImage(self.ghost4Img),
                      ImageTk.PhotoImage(self.ghost5Img),
                      ImageTk.PhotoImage(self.ghost6Img)]
        cherry = ImageTk.PhotoImage(self.cherryImg)


        self.canvas.delete('all')
        for x,column in enumerate(board):
            for y,cell in enumerate(column):
                if snacks[x][y] == 1 or self.snacksMem[x][y] == 1:
                    self.canvas.create_rectangle(offset+x*cellSize+8, offset+y*cellSize+8, offset+(x+1)*cellSize-8, offset+(y+1)*cellSize-8, 
                                                 outline="black", fill="yellow", width=2)
                if cell == CHERRY:
                    self.canvas.create_image(((x+0.5)*cellSize + offset,(y+0.5)*cellSize + offset), image=cherry)
                if cell == WALL:
                    self.canvas.create_rectangle(offset+x*cellSize+1, offset+y*cellSize+1, offset+(x+1)*cellSize-1, offset+(y+1)*cellSize-1, 
                                                 outline="black", fill="blue", width=2)
        
        for i, powerup in enumerate(powerUps):
            self.canvas.create_rectangle(offset+powerup[0]*cellSize+6, offset+powerup[1]*cellSize+6, offset+(powerup[0]+1)*cellSize-6, offset+(powerup[1]+1)*cellSize-6, 
                                         outline="black", fill="yellow", width=2)
        
        for i, powerup in enumerate(self.powerUpMem):
            self.canvas.create_rectangle(offset+powerup[0]*cellSize+6, offset+powerup[1]*cellSize+6, offset+(powerup[0]+1)*cellSize-6, offset+(powerup[1]+1)*cellSize-6, 
                                         outline="black", fill="yellow", width=2)
        
        for i, ghost in enumerate(ghosts):
            position =self.smoothMove(ghost, moveOffset, direction[i+1], moved[i+1])
            if powerUpCount == 0: self.canvas.create_image(((position[0]+0.5)*cellSize + offset, (position[1]+0.5)*cellSize + offset), image=ghostImges[i])
            elif powerUpCount < 5 and moveOffset > 0: self.canvas.create_image(((position[0]+0.5)*cellSize + offset, (position[1]+0.5)*cellSize + offset), image=ghostImges[5])
            else: self.canvas.create_image(((position[0]+0.5)*cellSize + offset, (position[1]+0.5)*cellSize + offset), image=ghostImges[4])

        position = self.smoothMove((player[0],player[1]), moveOffset, direction[0], moved[0])
        if moved[0]: self.canvas.create_image(((position[0]+0.5)*cellSize + offset, (position[1]+0.5)*cellSize + offset), image=pacman[moveOffset])        
        else: self.canvas.create_image(((position[0]+0.5)*cellSize + offset, (position[1]+0.5)*cellSize + offset), image=pacman[0])
        
        if moveOffset == 3:
            for i, row in enumerate(snacks):
                self.snacksMem[i] = [value for value in row]
            self.powerUpMem.clear()
            for pos in powerUps:
                self.powerUpMem.append(pos)

        self.canvas.create_rectangle(offset, BOARD_HEIGHT*cellSize+offset*2, BOARD_WIDTH*cellSize+offset, (BOARD_HEIGHT+1)*cellSize+offset*2, 
                                     outline="black", fill="gray", width=2)
        self.canvas.create_text(205, 420, text=f"Score: {score}")

        self.window.update()

    def titlePage(self):
        cellSize = 20
        arrows = ImageTk.PhotoImage(self.arrowsImg)

        self.canvas.create_text(200, 100, text="PAC-MAN", fill="black", font="Helvetica 32")
        self.canvas.create_image(BOARD_WIDTH / 2 * cellSize, BOARD_HEIGHT / 2 * cellSize, image=arrows)
        self.canvas.create_text(200, 300, text="UP, DOWN, LEFT, and RIGHT to move\nRUN from ghosts\neat SNACKS, CHERRIES, and POWER-UPs to win!", fill="black", font="Helvetica 12")

        self.window.update()
    
    def levelPage(self, level):
        self.canvas.delete('all')
        self.canvas.create_text(200, 100, text=f"Level {level}", fill="black", font="Helvetica 32")
        self.window.update()

if __name__ == "__main__":
    gui = GUI()
    gui.window.mainloop()