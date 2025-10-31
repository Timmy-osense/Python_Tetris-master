# encoding: utf-8
import os, sys, random
import time
import pygame 
from pygame.locals import *
from drew import *

# Constant - Brick rapid drop speed
BRICK_DROP_RAPIDLY   = 0.04
# Constant - Brick normal drop speed
BRICK_DOWN_SPEED_MAX = 0.5

# Canvas size
canvas_width = 800
canvas_height = 600

# Color
color_block         = (0,0,0)
color_white         = (255, 255, 255)
color_red           = (255, 0, 0)
color_gray          = (107,130,114)
color_gray_block    = (20,31,23)
color_gray_green    = (0, 255, 0)

# Define bricks
brick_dict = {
    "10": ( 4, 8, 9,13), "11": ( 9,10,12,13),   # N1.
    "20": ( 5, 8, 9,12), "21": ( 8, 9,13,14),   # N2.
    "30": ( 8,12,13,14), "31": ( 4, 5, 8,12), "32": (8,  9, 10, 14), "33": (5,  9, 12, 13), # L1.
    "40": (10,12,13,14), "41": ( 4, 8,12,13), "42": (8,  9, 10, 12), "43": (4,  5,  9, 13), # L2.
    "50": ( 9,12,13,14), "51": ( 4, 8, 9,12), "52": (8,  9, 10, 13), "53": (5,  8,  9, 13), # T.
    "60": ( 8, 9,12,13),    # O.
    "70": (12,13,14,15), "71": ( 1, 5, 9,13)    #I.
}

# Brick array (10x20)
bricks_array = []
for i in range(10):
    bricks_array.append([0]*20)
# Brick array (4x4)
bricks = []
for i in range(4):
    bricks.append([0]*4)
# Next brick array (4x4)
bricks_next = []
for i in range(4):
    bricks_next.append([0]*4)
# Next brick shape array (4x4)
bricks_next_object = []
for i in range(4):
    bricks_next_object.append([0]*4)    
# Brick count list
bricks_list = []
for i in range(10):
    bricks_list.append([0]*20)

# Brick position in container
# (-2~6) (Cannot rotate when x is 6)
container_x = 3
# (-3~16) (-3 means falling from above the boundary)
container_y =-4

# Debug message
debug_message = False
# Game over flag
game_over = False
# Game pause flag
game_paused = False

# Brick drop speed
brick_down_speed = BRICK_DOWN_SPEED_MAX

# Brick ID (1~7)
brick_id = 1
# Brick state (0~3)
brick_state = 0

# Next brick ID (1~7)
brick_next_id = 1

# Max lines cleared
lines_number_max = 0
# Current game lines cleared
lines_number = 0

# Game state
# 0: Game in progress
# 1: Clearing bricks
game_mode = 0

#-------------------------------------------------------------------------
# Function: Display text
# Input:
#   text    : String
#   x, y    : Coordinates
#   color   : Color
#-------------------------------------------------------------------------
def showFont( text, x, y, color):
    global canvas    
    text = font.render(text, True, color) 
    canvas.blit( text, (x,y))

#-------------------------------------------------------------------------
# Function: Get brick index array
# Input:
#   brickId : Brick ID (1~7)
#   state   : Brick state (0~3)
#-------------------------------------------------------------------------
def getBrickIndex( brickId, state):
    global brick_dict

    # Combine string
    brickKey = str(brickId)+str(state)
    # Return brick array
    return brick_dict[brickKey]

#-------------------------------------------------------------------------
# Convert defined brick to brick array
# Input:
#   brickId : Brick ID (1~7)
#   state   : Brick state (0~3)
#-------------------------------------------------------------------------
def transformToBricks( brickId, state):
    global bricks

    # Clear brick array
    for x in range(4):
        for y in range(4):
            bricks[x][y] = 0
     
    # Get brick index array
    p_brick = getBrickIndex(brickId, state)
    
    # Convert brick to brick array
    for i in range(4):        
        bx = int(p_brick[i] % 4)
        by = int(p_brick[i] / 4)
        bricks[bx][by] = brickId

    """
    # Print message
    for y in range(4): 
        s = ""
        for x in range(4): 
            s = s + str(bricks[x][y]) + ","       
        print(s)
    """

#-------------------------------------------------------------------------
# Check if brick can be copied to container
# Output:
#   true    : Can copy
#   false   : Cannot copy
#-------------------------------------------------------------------------
def ifCopyToBricksArray():
    global bricks, bricks_array
    global container_x, container_y

    posX = 0
    posY = 0
    for x in range(4):
        for y in range(4):
           if (bricks[x][y] != 0):
                posX = container_x + x
                posY = container_y + y
                if (posX >= 0 and posY >= 0):
                    try:
                        if (bricks_array[posX][posY] != 0):
                            return False
                    except:
                        return False
    return True

#-------------------------------------------------------------------------
# Copy brick to container
#-------------------------------------------------------------------------
def copyToBricksArray():
    global bricks, bricks_array
    global container_x, container_y
    
    posX = 0
    posY = 0
    for x in range(4):
        for y in range(4):
            if (bricks[x][y] != 0):
                posX = container_x + x
                posY = container_y + y
                if (posX >= 0 and posY >= 0):
                    bricks_array[posX][posY] = bricks[x][y]
     
#-------------------------------------------------------------------------
# Initialize game
#-------------------------------------------------------------------------
def resetGame():
    global BRICK_DOWN_SPEED_MAX
    global bricks_array, bricks, lines_number, lines_number_max

    # Clear brick array
    for x in range(10):
        for y in range(20):
            bricks_array[x][y] = 0
            
    # Clear brick array
    for x in range(4):
        for y in range(4):
            bricks[x][y] = 0

    # Initialize brick drop speed
    brick_down_speed = BRICK_DOWN_SPEED_MAX

    # Max lines cleared
    if(lines_number > lines_number_max):
        lines_number_max = lines_number
    # Lines cleared this game
    lines_number = 0

#---------------------------------------------------------------------------
# Check and set bricks to clear
# Output:
#   Number of lines cleared
#---------------------------------------------------------------------------
def ifClearBrick():
    pointNum = 0
    lineNum = 0
    for y in range(20):
        for x in range(10):
            if (bricks_array[x][y] > 0):
                pointNum = pointNum + 1
            if (pointNum == 10):
                for i in range(10):
                    lineNum = lineNum + 1
                    bricks_array[i][y] = 9
        pointNum = 0
    return lineNum

#-------------------------------------------------------------------------
# Update next brick
#-------------------------------------------------------------------------
def updateNextBricks(brickId):
    global bricks_next
    
    # Clear brick array
    for y in range(4):
        for x in range(4):
            bricks_next[x][y] = 0

    # Get brick index array
    pBrick = getBrickIndex(brickId, 0)

    # Convert brick to brick array
    for i in range(4):
        bx = int(pBrick[i] % 4)
        by = int(pBrick[i] / 4)
        bricks_next[bx][by] = brickId

    # Update background brick
    background_bricks_next.update()

    # Update brick image
    pos_y = 52
    for y in range(4):
        pos_x = 592
        for x in range(4):
            if(bricks_next[x][y] != 0):
                bricks_next_object[x][y].rect[0] = pos_x
                bricks_next_object[x][y].rect[1] = pos_y
                bricks_next_object[x][y].update()
            pos_x = pos_x + 28        
        pos_y = pos_y + 28
                
#-------------------------------------------------------------------------
# Generate new brick
#-------------------------------------------------------------------------
def brickNew():
    global game_over, container_x, container_y, brick_id, brick_next_id, brick_state
    global lines_number, game_mode

    # Check if game is over
    game_over = False
    if (container_y < 0):
        game_over = True

    # Copy brick to container
    container_y = container_y - 1
    copyToBricksArray()  
    
    #------------------------------------------------    
    # Check and set bricks to clear
    lines = ifClearBrick() / 10;        
    if (lines > 0):
        # Accumulate cleared lines
        lines_number =  lines_number + lines
        # Modify line count
        #modifyLabel(linesNumber, fontLinesNumber)
        # 1: Clear bricks
        game_mode = 1

    # Initialize brick position
    container_x = 3
    container_y =-4

    # Current brick
    brick_id = brick_next_id

    # Next brick
    # Brick ID (1~7)
    brick_next_id = random.randint( 1, 7)
    
    # Initialize brick state
    brick_state = 0

    # GameOver
    if (game_over):
        # Restart game
        resetGame()
    
#-------------------------------------------------------------------------
# Clear bricks
#-------------------------------------------------------------------------
def clearBrick():
    global bricks_array
    # Clear bricks line by line
    temp = 0    
    for x in range(10):
        for i in range(19):
            for y in range(20):
                if (bricks_array[x][y] == 9):
                    if (y > 0):
                        temp = bricks_array[x][y - 1]
                        bricks_array[x][y - 1] = bricks_array[x][y]
                        bricks_array[x][y] = temp
                        y = y - 1
            bricks_array[x][0] = 0
#-------------------------------------------------------------------------
# Initialize
pygame.init()
# Display title
pygame.display.set_caption(u"Tetris Game")
# Create canvas size
# Fullscreen mode
#canvas = pygame.display.set_mode((canvas_width, canvas_height), pygame.DOUBLEBUF and pygame.FULLSCREEN )
# Window mode
canvas = pygame.display.set_mode((canvas_width, canvas_height))

# Clock
clock = pygame.time.Clock()

# Check system supported fonts
#print(pygame.font.get_fonts())

# Set font - Helvetica
font = pygame.font.SysFont("simsunnsimsun", 24)


# Add drawing bricks to array
for y in range(20):
    for x in range(10):
        bricks_list[x][y] = Box(pygame, canvas, "brick_x_" + str(x) + "_y_" + str(y), [ 0, 0, 26, 26], color_gray_block)

# Add drawing bricks to array
for y in range(4):
    for x in range(4):
        bricks_next_object[x][y] = Box(pygame, canvas, "brick_next_x_" + str(x) + "_y_" + str(y), [ 0, 0, 26, 26], color_gray_block)

# Background brick
background = BoxRect(pygame, canvas, "background", [ 278, 18, 282, 562], color_gray)

# Background brick next
background_bricks_next = BoxRect(pygame, canvas, "background_bricks_next", [ 590, 50, 114, 114], color_gray)

# Brick ID (1~7)
brick_next_id = random.randint( 1, 7)
# Generate new brick
brickNew()

#-------------------------------------------------------------------------    
# Main loop
#-------------------------------------------------------------------------
running = True
time_temp = time.time()
time_now = 0
while running:
    # Calculate clock
    time_now = time_now + (time.time() - time_temp)
    time_temp = time.time()
    #---------------------------------------------------------------------
    # Check input
    #---------------------------------------------------------------------
    for event in pygame.event.get():
        # Exit game
        if event.type == pygame.QUIT:
            running = False        
        # Check key pressed
        if event.type == pygame.KEYDOWN:
            #-----------------------------------------------------------------
            # Check ESC button pressed
            if event.key == pygame.K_ESCAPE:
                running = False
            # Toggle debug message
            elif event.key == pygame.K_d:
                debug_message = not debug_message
            # Toggle pause - P key
            elif event.key == pygame.K_p:
                game_paused = not game_paused
            #-----------------------------------------------------------------
            # Rotate brick - Up
            elif event.key == pygame.K_UP and game_mode == 0 and not game_paused:
                # Cannot rotate at right boundary
                if (container_x == 8):
                    break
                # Check brick N1, N2, I
                if (brick_id == 1 or brick_id == 2 or brick_id == 7):
                    # Long brick rotation exception handling
                    if (brick_id == 7):
                        if (container_x < 0 or container_x == 7):
                            break
                    # Rotate brick
                    brick_state = brick_state + 1
                    if (brick_state > 1):
                        brick_state = 0                    
                    # Convert defined brick to brick array
                    transformToBricks(brick_id, brick_state)
                    # Hit brick
                    if (not ifCopyToBricksArray()):
                        brick_state = brick_state - 1
                        if (brick_state < 0):
                            brick_state = 1
                # Check brick L1, L2, T                                
                elif (brick_id == 3 or brick_id == 4 or brick_id == 5):
                    # Rotate brick
                    brick_state = brick_state + 1
                    if (brick_state > 3):
                        brick_state = 0                    
                    # Convert defined brick to brick array
                    transformToBricks(brick_id, brick_state)
                    # Hit brick
                    if (not ifCopyToBricksArray()):
                        brick_state = brick_state - 1
                        if (brick_state < 0):
                            brick_state = 3
            #-----------------------------------------------------------------
            # Fast drop - Down
            elif event.key == pygame.K_DOWN and game_mode == 0 and not game_paused:
                # Brick fast drop
                brick_down_speed = BRICK_DROP_RAPIDLY
            #-----------------------------------------------------------------
            # Move brick - Left (reversed logic: left key moves right)
            elif event.key == pygame.K_LEFT and game_mode == 0 and not game_paused:
                container_x = container_x + 1
                if (container_x > 6):
                    if (container_x == 7):
                        if (bricks[3][0] != 0 or bricks[3][1] != 0 or bricks[3][2] != 0 or bricks[3][3] != 0):
                            container_x = container_x - 1;
                    elif (container_x == 8):
                        if (bricks[2][0] != 0 or bricks[2][1] != 0 or bricks[2][2] != 0 or bricks[2][3] != 0):
                            container_x = container_x - 1
                    else:
                        container_x = container_x - 1
                # Hit brick
                if (not ifCopyToBricksArray()):
                    container_x = container_x - 1
            #-----------------------------------------------------------------
            # Move brick - Right (reversed logic: right key moves left)
            elif event.key == pygame.K_RIGHT and game_mode == 0 and not game_paused:
                container_x = container_x - 1
                if (container_x < 0):
                    if (container_x == -1):
                        if (bricks[0][0] != 0 or bricks[0][1] != 0 or bricks[0][2] != 0 or bricks[0][3] != 0):
                            container_x = container_x + 1
                    elif (container_x == -2):
                        if (bricks[1][0] != 0 or bricks[1][1] != 0 or bricks[1][2] != 0 or bricks[1][3] != 0):
                            container_x = container_x + 1
                    else:
                        container_x = container_x + 1
                # Hit brick
                if (not ifCopyToBricksArray()):
                    container_x = container_x + 1                    
        #-----------------------------------------------------------------
        # Check key released
        if event.type == pygame.KEYUP:
            # Fast drop - Down
            if event.key == pygame.K_DOWN and not game_paused:
                # Restore normal drop speed
                brick_down_speed = BRICK_DOWN_SPEED_MAX
        
    #---------------------------------------------------------------------    
    # Clear canvas
    canvas.fill(color_block)

    # In game and not paused
    if (game_mode == 0 and not game_paused):
        # Process brick drop
        if(time_now >= brick_down_speed):
            # Drop down
            container_y = container_y + 1; 
            # Hit brick
            if (not ifCopyToBricksArray()):
                #Generate new brick
                brickNew()            
            # Convert defined brick to brick array (bricks)
            transformToBricks( brick_id, brick_state)
            # Clear clock
            time_now = 0
    # Clear bricks
    elif (game_mode == 1 and not game_paused):
        # Clear bricks
        clearBrick()
        # In game
        game_mode = 0
        # Convert defined brick to brick array
        transformToBricks(brick_id, brick_state)

    #---------------------------------------------------------------------    
    # Update next brick shape
    updateNextBricks(brick_next_id)
    # Update drawing
    pos_y = 20
    # Update background brick
    background.update()
    for y in range(20):
        pos_x = 280
        for x in range(10):
            if(bricks_array[x][y] != 0):
                bricks_list[x][y].rect[0] = pos_x
                bricks_list[x][y].rect[1] = pos_y
                bricks_list[x][y].update()
            pos_x = pos_x + 28        
        pos_y = pos_y + 28    
    # Update brick
    for y in range(4):
        for x in range(4):            
            if (bricks[x][y] != 0):
                posX = container_x + x
                posY = container_y + y
                if (posX >= 0 and posY >= 0):
                    bricks_list[posX][posY].rect[0] = (posX * 28) + 280
                    bricks_list[posX][posY].rect[1] = (posY * 28) + 20
                    bricks_list[posX][posY].update()
    #---------------------------------------------------------------------    
    # Debug message
    if(debug_message):
        # Update container
        str_x = ""
        pos_x = 15
        pos_y = 20
        for y in range(20):
            str_x = ""
            for x in range(10):
                str_x = str_x + str(bricks_array[x][y]) + " "
            showFont( str_x, pos_x, pos_y, color_red)
            pos_y = pos_y + 28
            
        # Update brick
        posX = 0
        posY = 0    
        for y in range(4):
            str_x = ""
            for x in range(4):            
                if (bricks[x][y] != 0):
                    posX = container_x + x
                    posY = container_y + y
                    if (posX >= 0 and posY >= 0):
                        str_x = str_x + str(bricks[x][y]) + " "
                else:
                    str_x = str_x + "  "
            pos_x = 15 + (container_x * 26)
            pos_y = 20 + (posY * 28)
            showFont( str_x, pos_x, pos_y, color_white)

    # Display message
    showFont( u"Next Block", 588, 16, color_gray)

    showFont( u"Max Lines", 588, 190, color_gray)
    showFont( str(int(lines_number_max)), 588, 220, color_gray)

    showFont( u"Current Lines", 588, 260, color_gray)
    showFont( str(int(lines_number)), 588, 290, color_gray)

    # Display pause status
    if game_paused:
        showFont( u"PAUSED", 588, 330, color_red)
        showFont( u"Press P to resume", 588, 360, color_gray)
        # Display pause overlay in game area
        showFont( u"GAME PAUSED", 320, 280, color_red)
        showFont( u"Press P to Continue", 310, 320, color_white)
    else:
        showFont( u"Press P to pause", 588, 330, color_gray)

    # Display FPS
    # Debug message
    if(debug_message):    
        showFont( u"FPS:" + str(clock.get_fps()), 6, 0, color_gray_green)    

    # Update canvas
    pygame.display.update()
    clock.tick(60)

# Exit game
pygame.quit()
quit()