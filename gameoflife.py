import pygame
import time

screen_width = 600
screen_height = 600
gridBoxes = []
block_count = 30
blockSize = screen_width//block_count
spacing = 2
gen = 0
isUpdating = False
running = True

dead = (0,0,0)
alive = (255,255,255)


pygame.init()
screen = pygame.display.set_mode((screen_width,screen_height))
clock = pygame.time.Clock()
running = True

# Creating Grid

for i in range(block_count):
    row = []
    for j in range(block_count):
        x = j * blockSize 
        y = i * blockSize 
        rect = pygame.Rect(x,y,blockSize-spacing,blockSize-spacing)
        row.append({"rect":rect, "color":dead})
    gridBoxes.append(row)

def drawGrid():
    for row in gridBoxes:
        for box in row:
            pygame.draw.rect(screen,box["color"],box["rect"])

# Counting live and dead neighbours of a cell

def neighbours(x,y):
    liveCount = 0
    deadCount = 0

    for i in range(x-1,x+2):
        for j in range(y-1, y+2):
            if(i == x and j == y):
                continue
            if 0 <= i < block_count and 0 <= j < block_count:
                if gridBoxes[i][j]["color"] == alive:
                    liveCount += 1
                elif gridBoxes[i][j]["color"] == dead:
                    deadCount += 1

    return liveCount, deadCount

# Updating grid according to the rules

def updateGrid():
    newGrid = []
    global gridBoxes

    for i in range(block_count):
        newRow = []
        for j in range(block_count):
            liveCount , deadCount = neighbours(i,j)

            if(gridBoxes[i][j]["color"] == alive):
                if(liveCount < 2 or liveCount > 3):
                    newRow.append({"rect":gridBoxes[i][j]["rect"], "color":dead})
                else:
                    newRow.append({"rect":gridBoxes[i][j]["rect"], "color":alive})
            
            else:
                if(liveCount == 3):
                    newRow.append({"rect":gridBoxes[i][j]["rect"], "color":alive})
                else:
                    newRow.append({"rect":gridBoxes[i][j]["rect"], "color":dead})

        newGrid.append(newRow)

    gridBoxes = newGrid


while running:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            
            mouseX , mouseY = mouse_pos
            posX = mouseY // blockSize
            posY = mouseX // blockSize
            
            gridBoxes[posX][posY]["color"] = alive

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                
                isUpdating = not isUpdating

    if isUpdating:
        updateGrid()
        gen += 1
        print(f"Generation : {gen}")
        time.sleep(0.1)
            

    screen.fill("purple")
    drawGrid()
    pygame.display.flip()
    clock.tick(60)

pygame.quit()

